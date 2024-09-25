import numpy as np
import grismconf
import os
from astropy.io import fits
from scipy import sparse
from astropy.table import Table
#from NIRCAM_Gsim import polyclip
#from NIRCAM_Gsim.disperse import *
from ..disperse.disperse import dispersed_pixel
import h5py
from scipy.interpolate import interp1d
import platform
import multiprocessing
#import ray
from tqdm import tqdm
import psutil
import pickle

class interp1d_picklable(object):
    """ class wrapper for piecewise linear function
    """

    def __init__(self, xi, yi, **kwargs):
        self.xi = xi
        self.yi = yi
        self.args = kwargs
        self.f = interp1d(xi, yi, **kwargs)

    def __call__(self, xnew):
        return self.f(xnew)

    def __getstate__(self):
        return self.xi, self.yi, self.args

    def __setstate__(self, state):
        self.f = interp1d(state[0], state[1], **state[2])

def comprehension_flatten( aList ):
        return list(y for x in aList for y in x)

def helper(vars):
    x0s,y0s,f,order,C,ID,extrapolate_SED, xoffset, yoffset, outbound = vars # in this case ID is dummy number
    p = dispersed_pixel(x0s,y0s,f,order,C,ID,extrapolate_SED=extrapolate_SED,xoffset=xoffset,yoffset=yoffset,outbound=outbound)
    xs, ys, areas, lams, counts,ID = p
    IDs = [ID] * len(xs)

    pp = np.array([xs, ys, areas, lams, counts,IDs])
    return pp


# @ray.remote
# def mega_helper(pars):
#     return [helper(p) for p in pars]
    


class observation():
    # This class defines an actual observations. It is tied to a single flt and a single config file
    
    def __init__(self,mypool,direct_images,segmentation_data,config,mod="A",order="+1",plot=0,max_split=100,SED_file=None,extrapolate_SED=False,max_cpu=-1,ID=0,SBE_save=None, boundaries=[], outbound=False,renormalize=True, resample=True, multiprocessor='multiprocessing',seed_cube=None,save_objects=None):
        """direct_images: List of file name containing direct imaging data
        segmentation_data: an array of the size of the direct images, containing 0 and 1's, 0 being pixels to ignore
        config: The path and name of a GRISMCONF NIRCAM configuration file
        mod: Module, A or B
        order: The name of the spectral order to simulate, +1 or +2 for NIRCAM
        max_split: Number of chunks to compute instead of trying everything at once.
        SED_file: Name of HDF5 file containing datasets matching the ID in the segmentation file and each consisting of a [[lambda],[flux]] array.
        SBE_save: If set to a path, HDF5 containing simulated stamps for all obsjects will be saved.
        boundaries: a tuple containing the coordinates of the FOV within the larger seed image.
        multiprocessor: 'multiprocessing' for native Python.
        """
        print("direct_images:",direct_images)
        if not seed_cube is None:
            print("Seed images: 3D cube")
        #print("segmentation_data:",segmentation_data)
        print("config:",config)
        print("mod:",mod)
        print("order:",order)
        print("plot:",plot)
        print("max_split:",max_split)
        print("SED_file:",SED_file)
        print("extrapolate_SED:",extrapolate_SED)
        print("max_cpu:",max_cpu)
        print("ID:",ID)
        print("SBE_save:",SBE_save)
        print("boundaries:",boundaries)
        print("renormalize:",renormalize)
        print("resample:",resample)
        print("multiprocessor:",multiprocessor)


        if max_cpu<0:
            max_cpu = psutil.cpu_count(logical=False) 

        print("Loading grism configuration file:",config)
        self.C = grismconf.Config(config)
            
        if plot:
            import matplotlib.pyplot as plt
            plt.ion()
            plt.clf()
            x = np.arange(self.C.WMIN,self.C.WMAX,(self.C.WMAX,self.C.WMIN)/100.)
            plt.plot(x,self.C.SENS[order](x))

        self.ID = ID
        self.IDs = []
        self.dir_images = direct_images
        self.seg = segmentation_data
        self.c3d = seed_cube
        self.dims = np.shape(self.seg)
        self.outbound = outbound
        self.order = order
        self.SED_file = SED_file
        self.SBE_save = SBE_save
        self.max_cpu = max_cpu
        self.cache = False
        self.POM_mask = None
        self.POM_mask01 = None
        self.renormalize = renormalize
        self.resample = resample
        self.multiprocessor = multiprocessor 
        self.mypool = mypool
        self.save_objects = save_objects

        print("Ooutbound is",outbound)

        if self.C.POM is not None:
            print("Using POM mask",self.C.POM)
            with fits.open(self.C.POM) as fin:
                self.POM_mask = fin[1].data
                self.POM_mask01 = fin[1].data * 1. # A version of the mask that only contains 0-1 values. Pixels with labels/values>10000 are set to 1.
                self.POM_mask01[self.POM_mask01>=10000] = 1.
                self.Pxstart = int(fin[1].header["NOMXSTRT"])
                self.Pxend = int(fin[1].header["NOMXEND"])
                self.Pystart = int(fin[1].header["NOMYSTRT"])
                self.Pyend = int(fin[1].header["NOMYEND"])

                if len(fin)>2:
                    self.POM_transmission = {}
                    for i in range(2,len(fin)):
                        try:
                            w = fin[i].data["Wavelength"]
                            t = fin[i].data["Transmission"]
                            indx = int(fin[i].header["POMINDX"])
                            self.POM_transmission[indx] = interp1d_picklable(w,t,bounds_error=False,fill_value=0.)
                            print("Loading extra optical element transmission curves from POM file extension {}".format(i))
                        except:
                            pass

        if len(boundaries)!=4:           
            xpad = (np.shape(segmentation_data)[1]-self.C.NAXIS[0])//2
            ypad = (np.shape(segmentation_data)[0]-self.C.NAXIS[1])//2
            self.xstart = 0 + xpad
            self.xend = xpad + self.C.NAXIS[0]-1
            self.ystart = 0 + ypad
            self.yend = ypad + self.C.NAXIS[1]-1
            print("No boundaries passed. Assuming symmetrical padding of {} {} pixels and a final size of {} {} .".format(xpad,ypad,self.xend+1-self.xstart,self.yend+1-self.ystart))
        else:
            self.xstart,self.xend,self.ystart,self.yend = boundaries

        
        self.extrapolate_SED = extrapolate_SED # Allow for SED extrapolation
        if self.extrapolate_SED:
            print("Warning: SED Extrapolation turned on.")
        if self.renormalize is False:
            print("Warning: not re-normalizing sources to unity")
            
        # if self.multiprocessor=='ray':
        #     print("Using ray for multiprocessing")
        #     ray.init(num_cpus=self.max_cpu,ignore_reinit_error=True)

        self.apply_POM()
        # self.create_pixel_list()
        
        self.p_l = []
        self.p_a = []


    def apply_POM(self):
        """Account for the finite size of the POM and remove pixels in segmentation files which should not
        be dispersed.
        If a POM mask array was loaded then we make sure it is modified to have the same size as the input seg map
        and with the detector FOV starting at the same pixel locations as the input seg map."""

        if self.POM_mask is None:
            x0 = int(self.xstart+self.C.XRANGE[self.C.orders[0]][0] + 0.5)
            x1 = int(self.xend+self.C.XRANGE[self.C.orders[0]][1] + 0.5)
            y0 = int(self.ystart+self.C.YRANGE[self.C.orders[0]][0] + 0.5)
            y1 = int(self.yend+self.C.YRANGE[self.C.orders[0]][1] + 0.5)

            if x0<0: x0 = 0
            if y0<0: y0 = 0
            ymax,xmax = np.shape(self.seg)
            if x0+1>xmax: x0 = xmax-1
            if y0+1>ymax: y0 = ymax-1

            from astropy.io import fits
            print("POM footprint applied: [{}:{},{}:{}]".format(x0,x1,y0,y1))
            print("Pixels outside of this region of the input data ([{},{}]) will not be dispersed.".format(xmax,ymax))
            self.seg[:,:x0+1] = 0
            self.seg[:,x1:] = 0
            self.seg[:y0+1,:] = 0
            self.seg[y1:,:] = 0
            
            if not self.c3d is None:
                for k in self.c3d.keys():
                    sx0,sy0,dsata,sseg = self.c3d[k]
                    sx1 = sx0 + np.shape(sseg)[1]
                    sy1 = sy0 + np.shape(sseg)[0]
                    self.c3d[k][3] = self.c3d[k][3] * self.seg[sy0:sy1,sx0:sx1]

        else:
            self.Pxstart - self.xstart
            self.Pystart - self.ystart

            ys1,xs1 = np.shape(self.POM_mask)
            ys2,xs2 = np.shape(self.seg)

            #print("xstart ettc:",self.xstart,self.xend,self.ystart,self.yend)
            #print("POM start etc:",self.Pxstart ,self.Pxend,self.Pystart ,self.Pyend)
            #print(self.Pystart - self.ystart,self.yend-self.ystart,self.Pxstart - self.xstart+1,self.xend-self.xstart+1)
            if (xs1>xs2) or (ys1>ys2):
                print("Warning: The input seg map is smaller ({},{}) than the POM mask ({},{}) for this mode.".format(xs2,ys2,xs1,ys1))
                raise Exception("Invalid seg map size.")

            # Crate a new POM mask that is the size of the input seg and data arrays
            # Compute the offset between where the detector is in the original POM mask and the input sef file
            xoff = self.xstart - self.Pxstart
            yoff = self.ystart - self.Pystart

            if (xoff<0) or (yoff<0):
                print("Warning: the input seg map and POM mask are not compatible. The seg map needs a larger border around the detector FOV than the POM mask.")
                print("seg map detector FOV starts at {} {}".format(self.xstart,self.ystart))
                print("POM mask detector FOV starts at {} {}".format(self.Pxstart,self.Pystart))
                raise Exception("Invalid seg map size.")
 
            POM = np.zeros(np.shape(self.seg))
            POM[yoff:yoff+ys1,xoff:xoff+xs1] = self.POM_mask
            self.POM_mask = POM*1

            # POM = np.zeros(np.shape(self.seg))
            # POM[yoff:yoff+ys1,xoff:xoff+xs1] = self.POM_mask
            POM[POM>1] = 1
            self.POM_mask01 = POM*1

            self.Pxstart  = self.xstart
            self.Pxend  = self.xend
            self.Pystart  = self.ystart
            self.Pyend  = self.ystart

            # We apply the POM mask to the seg file, but only as a mask, romving pixels getting no lights. We keep the POM mask with its orginal values otherwise 
            # to be able to account for partial transmission later on.
    

            #from astropy.io import fits
            #print("POM size:",np.shape(POM))
            #print("seg size:",np.shape(self.seg))
            #fits.writeto("seg_org.fits",self.seg,overwrite=True)
            mask = np.zeros(np.shape(self.POM_mask01),int)
            mask[self.POM_mask01>0] = 1
            self.seg = self.seg * mask
            #fits.writeto("POM_msk.fits",self.POM_mask,overwrite=True)
            #fits.writeto("POM.fits",self.POM_mask01 ,overwrite=True)
            #fits.writeto("seg_msk.fits",self.seg,overwrite=True)
            if not self.c3d is None:
                for k in self.c3d.keys():
                    sx0,sy0,dsata,sseg = self.c3d[k]
                    sx1 = sx0 + np.shape(sseg)[1]
                    sy1 = sy0 + np.shape(sseg)[0]
                    self.c3d[k][3] = self.c3d[k][3] * mask[sy0:sy1,sx0:sx1]

    def create_pixel_list(self):
        # Create a list of pixels to dispersed, grouped per object ID



        if not self.c3d is None:
            print("Using seed cube")
            self.create_pixel_list_from_seed_cube()
            return

        if self.save_objects is not None and os.path.isfile(self.save_objects):
            print("Loading from pre-computed ",self.save_objects)
            self.IDs,self.xs,self.ys,self.fs = pickle.load(open(self.save_objects,"rb"))
            return

        if self.ID==0:
            self.xs = []
            self.ys = []
            all_IDs = np.array(list(set(np.ravel(self.seg))))
            all_IDs = all_IDs[all_IDs>0]

            # Remove
            # self.IDs = self.IDs[0:10]
            # all_IDs = all_IDs[0:10]
            #

            print("We have ",len(all_IDs),"Objects")
            for ID in tqdm(all_IDs):
                ys,xs = np.nonzero(self.seg==ID)

                if (len(xs)>0) & (len(ys)>0):
                    self.xs.append(xs)
                    self.ys.append(ys)
                    self.IDs = all_IDs
        else:
            vg = self.seg==self.ID
            ys,xs = np.nonzero(vg)            
           
            if (len(xs)>0) & (len(ys)>0):    
                self.xs.append(xs)
                self.ys.append(ys)
                self.IDs = [self.ID]

        self.fs = {}
        for dir_image in self.dir_images:
            print("dir image:",dir_image)
            if self.SED_file==None:
                try:
                    l = fits.getval(dir_image,'PHOTPLAM') / 10000. # in Angsrrom and we want Micron now
                except:
                    print("WARNING: unable to find PHOTPLAM keyword in {}".format(dir_image))
                    sys.exit()

                try:
                    photflam = fits.getval(dir_image,'photflam')
                except:
                    print("WARNING: unable to find PHOTFLAM keyword in {}".format(dir_image))
                    sys.exit()
                print("Loaded",dir_image, "wavelength:",l,"micron")

            try:
                d = fits.open(dir_image)[1].data
            except:
                d = fits.open(dir_image)[0].data

            # If we do not use an SED file then we use photometry to get fluxes
            # Otherwise, we assume that objects are normalized to 1.
            if self.SED_file==None:
                self.fs[l] = []
                dnew = d
                if self.POM_mask01 is not None:
                    dnew = d * self.POM_mask01 # Apply POM transmission mask to the data pixels

                for i in range(len(self.IDs)):
                    self.fs[l].append(dnew[self.ys[i],self.xs[i]] * photflam)

            else:
                # Need to normalize the object stamps              
                for ID in tqdm(self.IDs,desc='Normalizing objects footprint'):
                    vg = self.seg==ID
                    dnew = d
                    
                    if self.renormalize is True:
                        sum_seg = np.sum(dnew[vg]) # But normalize by the whole flux
                        if sum_seg!=0.:
                            dnew[vg] = dnew[vg]/sum_seg
                    # else:
                    #     print("not re-normalizing sources to unity")

                    if self.POM_mask01 is not None:
                        #print("Applying POM transmission to data")
                        dnew = dnew * self.POM_mask01 # Apply POM transmission mask to the data pixels. This is a single grey correction for the whole object.

                self.fs["SED"] = []
                for i in range(len(self.IDs)):
                    self.fs["SED"].append(dnew[self.ys[i],self.xs[i]])
        if self.save_objects is not None:
            print("Saving pre-computed objects to ",self.save_objects)
            pickle.dump([self.IDs, self.xs,self.ys,self.fs],open(self.save_objects,"wb"))

        print("Done")

    def create_pixel_list_from_seed_cube(self):
        # Create a list of pixels to dispersed, grouped per object ID
        dir_image = self.dir_images[0]
        if self.SED_file==None:
            try:
                l = fits.getval(dir_image,'PHOTPLAM') / 10000. # in Angsrrom and we want Micron now
            except:
                print("WARNING: unable to find PHOTPLAM keyword in {}".format(dir_image))
                sys.exit()

            try:
                photflam = fits.getval(dir_image,'photflam')
            except:
                print("WARNING: unable to find PHOTFLAM keyword in {}".format(dir_image))
                sys.exit()
            print("Loaded",dir_image, "wavelength:",l,"micron")
            
        if self.ID==0:
            self.IDs = np.array(list(set(np.ravel(self.seg))))
            self.IDs = self.IDs[self.IDs>0]
        else:
            self.IDs = [self.ID]


        self.xs = []
        self.ys = []
        self.fs = {}

        if self.SED_file==None:
            self.fs[l] = []
        else:
            self.fs["SED"] = []

        print("We have ",len(self.IDs),"Objects")
        for ID in self.IDs:
            data_stp = self.c3d[ID][2]*1
            seg_stp = self.c3d[ID][3]*1
            ys0,xs0 = np.nonzero(seg_stp>0)
            xs = xs0 + self.c3d[ID][0]
            ys = ys0 + self.c3d[ID][1]
            # Coords in full frame
            xmin = self.c3d[ID][0]
            ymin = self.c3d[ID][1]
            xmax = xmin + np.shape(data_stp)[1]
            ymax = ymin + np.shape(data_stp)[0]

            self.xs.append(xs)
            self.ys.append(ys)
        
            if self.POM_mask01 is not None:
                data_stp = data_stp * self.POM_mask01[ymin:ymax,xmin:xmax]

            # If we do not use an SED file then we use photometry to get fluxes
            # Otherwise, we assume that objects are normalized to 1.
            if self.SED_file==None:
                    self.fs[l].append(data_stp[ys0,xs0] * photflam)
            else:
                # Need to normalize the object stamps                                  
                if self.renormalize is True:
                    sum_data_stp = np.sum(data_stp) # But normalize by the whole flux
                    if sum_data_stp!=0.:
                        data_stp = data_stp/sum_data_stp
                self.fs["SED"].append(data_stp[ys0,xs0])
    
    def disperse_all(self,cache=False):

        if cache:
            print("Object caching ON")
            self.cache = True
            self.cached_object = {}

        self.simulated_image = np.zeros(self.dims,float)
        
        self.create_pixel_list()
        
        for i in tqdm(range(len(self.IDs)),desc='Dispersing order {}'.format(self.order)):
            if self.cache:
                self.cached_object[i] = {}
                self.cached_object[i]['x'] = []
                self.cached_object[i]['y'] = []
                self.cached_object[i]['f'] = []
                self.cached_object[i]['w'] = []
                self.cached_object[i]['minx'] = []
                self.cached_object[i]['maxx'] = []
                self.cached_object[i]['miny'] = []
                self.cached_object[i]['maxy'] = []

            this_object = self.disperse_chunk(i)

            if self.SBE_save != None:
                # If SBE_save is enabled, we create an HDF5 file containing the stamp of this simulated object
                # order is in self.order
                # We just save the x,y,f,w arrays as well as info about minx,maxx,miny,maxy
    
                # We trim the stamp to avoid padding area
                this_SBE_object =  this_object[self.ystart:self.yend+1,self.xstart:self.xend+1]
                
                yss,xss = np.nonzero(this_SBE_object>0)
                
                if len(xss)<1:
                    continue 

                minx = np.min(xss)
                maxx = np.max(xss)
                miny = np.min(yss)
                maxy = np.max(yss)

                this_SBE_object = this_SBE_object[miny:maxy+1,minx:maxx+1]

                if os.path.isfile(self.SBE_save):
                    mode = "a"
                else:
                    mode = "w"

                with h5py.File(self.SBE_save,mode) as fhdf5:
                    dset = fhdf5.create_dataset("%d_%s" % (self.IDs[i],self.order),data=this_SBE_object,dtype='f',compression="gzip",compression_opts=9)
                    dset.attrs[u'minx'] = minx
                    dset.attrs[u'maxx'] = maxx
                    dset.attrs[u'miny'] = miny
                    dset.attrs[u'maxy'] = maxy
                    dset.attrs[u'units'] = 'e-/s'


    def disperse_background_1D(self,background):
        """Method to create a simple disperse background, obtained by dispersing a full row or column.
        We assume no field dependence in the cross dispersion direction and create a full 2D image by tiling a single dispersed row or column"""

        # Create a fake object, line in middle of detector
        C = self.C
        naxis = [self.xend-self.xstart+1 ,self.yend-self.ystart+1] 
        xpos,ypos = naxis[0]//2,naxis[1]//2

        # Find out if this an x-direction or y-direction dispersion
        dydx = np.array(C.DISPXY(self.order,1000,1000,1))-np.array(C.DISPXY(self.order,1000,1000,0))
        if np.abs(dydx[0])>np.abs(dydx[1]):
            #print("disperse_background_1D: x-direction")
            direction = "x"
            xs = np.arange(self.C.XRANGE[self.order][0]+0,self.C.XRANGE[self.order][1]+naxis[0])
            ys = np.zeros(np.shape(xs))+ypos
        else:
            #print("disperse_background_1D: y-direction")
            direction = "y"
            ys = np.arange(self.C.YRANGE[self.order][0]+0,self.C.YRANGE[self.order][1]+naxis[0])
            xs = np.zeros(np.shape(ys))+xpos

        #print(xpos,ypos)
        
        
        lam = background[0]
        fnu = background[1]

        fnu = fnu/4.25e10 # MJy/arcsec^2
        fnu = fnu*1e6 # Jy/arcsec^2
        fnu = fnu * (0.065**2) # Jy/pixel

        fnu = fnu*1e-23
        c = 299792458.* 1e10 # A
        wa = lam*10000
        flam = fnu/(wa**2/c)

        f = [lam,flam]
                
        pars = []        
        for i in range(len(xs)):
            ID = 1
            xs0 = [xs[i],xs[i]+1,xs[i]+1,xs[i]]
            ys0 = [ys[i],ys[i],ys[i]+1,ys[i]+1]
            pars.append([xs0,ys0,f,self.order,C,ID,False,self.xstart,self.ystart,self.outbound])


        bck = np.zeros(naxis,float)

        chunksize = int(len(pars)/self.max_cpu)
        if chunksize<1:
            chunksize = 1
        # if self.multiprocessor=='ray':
        #     #ray.init(num_cpus=self.max_cpu,ignore_reinit_error=True)
            
        #     chunked_pars = [pars[i * chunksize:(i + 1) * chunksize] for i in range((len(pars) + chunksize - 1) // chunksize )] 

        #     result_ids = []
        #     [result_ids.append(mega_helper.remote(cpars)) for cpars in chunked_pars]

        #     results = ray.get(result_ids)
        #     results = [item for sublist in results for item in sublist]

        #     del result_ids
        #     ##ray.shutdown()
        # else:
        for pp in self.mypool.imap_unordered(helper, pars, chunksize=chunksize):
            if np.shape(pp.transpose())==(1,6):
                continue
            
            x,y,w,f = pp[0],pp[1],pp[3],pp[4]

            vg = (x>=0) & (x<naxis[0]) & (y>=0) & (y<naxis[1]) 

            x = x[vg]
            y = y[vg]
            f = f[vg]
            w = w[vg]
                    
            if len(x)<1:
                continue

            minx = int(min(x))
            maxx = int(max(x))
            miny = int(min(y))
            maxy = int(max(y))
            a = sparse.coo_matrix((f, (y-miny, x-minx)), shape=(maxy-miny+1,maxx-minx+1)).toarray()
            bck[miny:maxy+1,minx:maxx+1] = bck[miny:maxy+1,minx:maxx+1] + a

        if direction=="x":
            bck = np.sum(bck,axis=0)
            bck = np.tile(bck,[naxis[1],1])
        else:
            bck = np.sum(bck,axis=1)
            bck = np.tile(bck,[naxis[0],1]).transpose()

        return bck

    def smooth(self,w,f,dw=0.002):
        from scipy.interpolate import interp1d
        from astropy.convolution import Gaussian1DKernel
        from astropy.convolution import convolve
        fct = interp1d(w,f)
        xs = np.arange(np.min(w),np.max(w),1./10000)
        ys = fct(xs)
        kernel = Gaussian1DKernel(stddev=dw)
        conv = convolve(ys,kernel)
        fct2 = interp1d(xs,conv)
        xs2 = np.arange(np.min(xs),np.max(xs),dw)
        ys2 = fct2(xs2)
        return xs2,ys2

    def disperse_chunk(self,c):
        """Method that handles the dispersion. To be called after create_pixel_list()"""
        import time


        if self.SED_file!=None:
            # We use an input spectrum file
            import h5py
            with h5py.File(self.SED_file,'r') as h5f:
                pars = []
                ###ID = int(self.seg[self.ys[c][0],self.xs[c][0]])
                ID = int(self.IDs[c])
                tmp = h5f["%s" % (ID)][:]

                if self.resample:
                    

                    # Figuring out a few things about size of order, dispersion and wavelengths to use    
                    wmin = self.C.WRANGE[self.order][0]
                    wmax = self.C.WRANGE[self.order][1]

                    t0 = self.C.INVDISPL(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,wmin)
                    t1 = self.C.INVDISPL(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,wmax)
                    
                    dx0 = self.C.DISPX(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,t0) - self.C.DISPX(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,t1)
                    dx1 = self.C.DISPY(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,t0) - self.C.DISPY(self.order,self.C.NAXIS[0]/2,self.C.NAXIS[1]/2,t1)

                    dw = np.abs((wmax-wmin)/(dx1-dx0))
                    print("Smoothing and resampling input spectrum to {} micron".format(dw))
                    # print("self.SED_file:",self.SED_file)
                    # print("lams:",tmp[0])
                    # print(tmp[0][1:]-tmp[0][:-1])
                    # print("DW:",dw)

                    tmp = self.smooth(tmp[0],tmp[1],dw/1.5)
                    #print(len(tmp[0]),len(tmp[1]))
                    
                
                ok = (tmp[0]>self.C.WRANGE[self.order][0]) & (tmp[0]<self.C.WRANGE[self.order][1])                        
                tmp = [tmp[0][ok],tmp[1][ok]]

                for i in range(len(self.xs[c])):
                    
                    lams = tmp[0]
                    fffs = tmp[1]*self.fs["SED"][c][i]
   
                    # trim input spectrum 
                    # try:
                    #     ok = (lams>self.C.WRANGE["+1"][0]) & (lams<self.C.WRANGE["+1"][1])
                    # except:
                    #     ok = (lams>self.C.WRANGE["A"][0]) & (lams<self.C.WRANGE["A"][1])

                    # ok = (lams>self.C.WRANGE[self.order][0]) & (lams<self.C.WRANGE[self.order][1])                        
                    # lams = lams[ok]
                    # fffs = fffs[ok]
                    #print(len(lams))
                    #sys.exit(1)
                    if self.POM_mask is not None:
                        POM_value = self.POM_mask[self.ys[c][i],self.xs[c][i]]
                    else:
                        POM_value = 1.
                    if POM_value>=10000:
                        #print("Applying additional transmission of :",self.xs[c][i],self.ys[c][i],POM_value)
                        trans = self.POM_transmission[POM_value](lams)
                        fffs = fffs * trans
                    else:
                        fffs = fffs * POM_value

                    if len(lams)>0:
                        f = [lams,fffs]
                        xs0 = [self.xs[c][i],self.xs[c][i]+1,self.xs[c][i]+1,self.xs[c][i]]
                        ys0 = [self.ys[c][i],self.ys[c][i],self.ys[c][i]+1,self.ys[c][i]+1]
                        pars.append([xs0,ys0,f,self.order,self.C,ID,self.extrapolate_SED,self.xstart,self.ystart,self.outbound])
        else:
            # No spectrum passed
            pars = []
            for i in range(len(self.xs[c])):
                ID = i
                xs0 = [self.xs[c][i],self.xs[c][i]+1,self.xs[c][i]+1,self.xs[c][i]]
                ys0 = [self.ys[c][i],self.ys[c][i],self.ys[c][i]+1,self.ys[c][i]+1]
                lams = np.array(list(self.fs.keys()))
                flxs = np.array([self.fs[l][c][i] for l in self.fs.keys()])
                ok = flxs!=0 # We avoid any pixel containing pure 0's
                if len(flxs[ok])==0: continue
                flxs = flxs[ok]
                lams = lams[ok]
                ok = np.argsort(lams)
                flxs = flxs[ok]
                lams = lams[ok]

                if self.POM_mask is not None:
                    POM_value = self.POM_mask[self.ys[c][i],self.xs[c][i]]
                else:
                    POM_value = 1.
                if POM_value>10000:
                    #print("Applying additional transmission of :",self.xs[c][i],self.ys[c][i],POM_value)
                    trans = self.POM_transmission[POM_value](lams)
                    flxs = flxs * trans
                else:
                    flxs = flxs * POM_value

                if len(lams)>0:
                    f = [lams,flxs]
                    pars.append([xs0,ys0,f,self.order,self.C,ID,self.extrapolate_SED,self.xstart,self.ystart,self.outbound])

        time1 = time.time()

        this_object = np.zeros(self.dims,float)
        chunksize = int(len(pars)/self.max_cpu)
        if chunksize<1:
            chunksize = 1

        chunksize = 10
        #print(len(pars),self.max_cpu,chunksize)
        if self.multiprocessor=='ray':
#            ray.init(num_cpus=self.max_cpu,ignore_reinit_error=True)

            chunked_pars = [pars[i * chunksize:(i + 1) * chunksize] for i in range((len(pars) + chunksize - 1) // chunksize )] 

            result_ids = []
            [result_ids.append(mega_helper.remote(cpars)) for cpars in chunked_pars]
            
            results = ray.get(result_ids)
            results = [item for sublist in results for item in sublist]

            del result_ids
            #ray.shutdown()
        else:
            #with multiprocessing.Pool(processes=self.max_cpu) as mypool:
            for pp in self.mypool.imap_unordered(helper, pars, chunksize=chunksize):
                if np.shape(pp.transpose())==(1,6):
                    continue
    
                x,y,w,f = pp[0],pp[1],pp[3],pp[4]

                vg = (x>=0) & (x<self.dims[1]) & (y>=0) & (y<self.dims[0]) & (np.isfinite(f)) 

                x = x[vg]
                y = y[vg]
                f = f[vg]
                w = w[vg]
                    
                if len(x)<1:
                    continue
                    
                minx = int(min(x))
                maxx = int(max(x))
                miny = int(min(y))
                maxy = int(max(y))
                a = sparse.coo_matrix((f, (y-miny, x-minx)), shape=(maxy-miny+1,maxx-minx+1)).toarray()
                self.simulated_image[miny:maxy+1,minx:maxx+1] = self.simulated_image[miny:maxy+1,minx:maxx+1] + a
                this_object[miny:maxy+1,minx:maxx+1] = this_object[miny:maxy+1,minx:maxx+1] + a

                if self.cache:
                    self.cached_object[c]['x'].append(x)
                    self.cached_object[c]['y'] .append(y)
                    self.cached_object[c]['f'].append(f)
                    self.cached_object[c]['w'].append(w)
                    self.cached_object[c]['minx'].append(minx)
                    self.cached_object[c]['maxx'].append(maxx)
                    self.cached_object[c]['miny'].append(miny)
                    self.cached_object[c]['maxy'].append(maxy)
            
        time2 = time.time()

        return this_object

    def disperse_all_from_cache(self,trans=None):
        if not self.cache:
            print("No cached object stored.")
            return

        self.simulated_image = np.zeros(self.dims,float)

        for i in tqdm(range(len(self.IDs)),desc="Dispersing order {} from cache".format(self.order)):
            this_object = self.disperse_chunk_from_cache(i,trans=trans)


    def disperse_chunk_from_cache(self,c,trans=None):
        """Method that handles the dispersion. To be called after create_pixel_list()"""
        
        import time

        if not self.cache:
            print("No cached object stored.")
            return

        time1 = time.time()
        
        this_object = np.zeros(self.dims,float)

        if trans!=None:
                print("Applying a transmission function...")
        for i in range(len(self.cached_object[c]['x'])): 
            x = self.cached_object[c]['x'][i]
            y = self.cached_object[c]['y'][i]
            f = self.cached_object[c]['f'][i]*1.
            w = self.cached_object[c]['w'][i]

            if trans!=None:
                f *= trans(w)

            minx = self.cached_object[c]['minx'][i]
            maxx = self.cached_object[c]['maxx'][i]
            miny = self.cached_object[c]['miny'][i]
            maxy = self.cached_object[c]['maxy'][i]
   
            a = sparse.coo_matrix((f, (y-miny, x-minx)), shape=(maxy-miny+1,maxx-minx+1)).toarray()
            self.simulated_image[miny:maxy+1,minx:maxx+1] = self.simulated_image[miny:maxy+1,minx:maxx+1] + a
            this_object[miny:maxy+1,minx:maxx+1] = this_object[miny:maxy+1,minx:maxx+1] + a

        time2 = time.time()

        print(time2-time1,"s.")
        return this_object

    def show(self):
        import matplotlib.pyplot as plt
        plt.ion()

        xx = self.p_x - min(self.p_x)
        yy = self.p_y - min(self.p_y)
        a = sparse.coo_matrix((self.p_f, (yy, xx)), shape=(max(yy)+1, max(xx)+1)).toarray()

        im = plt.imshow(a)
        im.set_clim(0,1)

        plt.draw()
        raw_input("...")

