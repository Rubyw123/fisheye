#include "fish2persp.h"

/*
	Turn a fisheye image (or partial fisheye) into a perspective
	projection with a certain field of view (FOV) and aspect ratio. Use
	supersmapling antialiasing, support different fisheye and
	perspective camera FOV, support off center fisheyes.
	X axis is to right, y axis inwards, z axis up
	February 2016: added pan and tilt, rotate about x (tilt) and then z (pan)
	Mar 2016: removed limit to 180 degree fisheye
	Apr 2016: added rotate about inward axis
	Aug 2016: added arbitrary rotation order support and efficiencies
	Aug 2016: Changed location of coordinate origin, now top-left
	May 2017: Added jpeg and new bitmaplib
	Aug 2017: Remove warp and lookup code
             Parameter cleanup
             Add support for anamorphic lenses, non circular fisheye
	Oct 2017: Added fourth order lens correction, needed for Entaniya 250 lens
   Mar 2019: Added PNG support, needs more testing
	Aug 2020: Adjusted how non circular fisheyes are handled\n");
	Sep 2020: Filled out params and fixed missing width bug
             Added remap filters
             For example: ffmpeg -i sample.jpg -i x.pgm -i y.pgm -lavfi remap sample.png
*/

// Input image 
BITMAP4 *fishimage = NULL;

// Output image
BITMAP4 *perspimage = NULL;

// Rotation transformations
TRANSFORM *transform = NULL;
int ntransform = 0;

PARAMS params;


int main(int argc,char **argv)
{
   int w,h,depth;
   char basename[256], fname[128];
   PARAMS *tmp = NULL;
   FILE *fptr;
	Init();
   // Test
   params.perspwidth = 1000;
   params.perspheight = 800
   params.fishfov = 190
   params.fishradius = 553
   params.fishcenterx = 1000
   params.fishcentery = 548

   transform = new TRANSFORM[2];
   transform[0].axis = XTILT;
   transform[0].value = 40.0;

   transform[1].axis = YROLL;
   transform[1].value = 30.0;

   basename = '5';
   fname = '5.jpg';

   transform = transform(transform,2);
   tmp = open_fish_image(params,fname, fptr,w,h,depth);
   perspimage = create_persp_image(perspimage);
   perspimage = convert(params,perspimage);
   write_file(params,fptr,fname,basename,perspimage);




	
	exit(0);
}

TRANSFORM* transform(TRANSFORM* transform[], int ntransform)
{
    int j;
    for (j=0;j<ntransform;j++) {
      transform[j].cvalue = cos(transform[j].value);
      transform[j].svalue = sin(transform[j].value);
   }
   return transform;
}

PARAMS open_fish_image(PARAMS params, char fname[], FILE * fptr, int w, int h, int depth)
{
    if (IsJPEG(fname))
		params.imageformat = JPG;
#ifdef ADDPNG
   if (IsPNG(fname))
      params.imageformat = PNG;
#endif
	if ((fptr = fopen(fname,"rb")) == NULL) {
		fprintf(stderr,"Failed to open fisheye image \"%s\"\n",fname);
		exit(-1);
	}
	if (params.imageformat == JPG) {
		JPEG_Info(fptr,&w,&h,&depth);
#ifdef ADDPNG
   } else if (params.imageformat == PNG) {
      PNG_Info(fptr,&w,&h,&depth);
#endif
   } else {
      TGA_Info(fptr,&w,&h,&depth);
	}
	if ((fishimage = Create_Bitmap(w,h)) == NULL) {
      fprintf(stderr,"Failed to allocate memory for fisheye image\n");
      exit(-1);
   }
	if (params.imageformat == JPG) {
      if (JPEG_Read(fptr,fishimage,&w,&h) != 0) {
         fprintf(stderr,"Failed to read fisheye JPG image\n");
         exit(-1);
      }
#ifdef ADDPNG
   } else if (params.imageformat == PNG) {
      if (PNG_Read(fptr,fishimage,&w,&h) != 0) {
         fprintf(stderr,"Failed to read fisheye PNG image\n");
         exit(-1);
      }
#endif
	} else {
		if (TGA_Read(fptr,fishimage,&w,&h) != 0) {
   	   fprintf(stderr,"Failed to read fisheye TGA image\n");
   	   exit(-1);
   	}
	}
	fclose(fptr);
    params.fishwidth = w;
	params.fishheight = h;

    return params;
}

BITMAP4* create_persp_image(BITMAP4* perspimage)
{
    if ((perspimage = Create_Bitmap(params.perspwidth,params.perspheight)) == NULL) {
      fprintf(stderr,"Failed to malloc perspective image\n");
      exit(-1);
   }
   Erase_Bitmap(perspimage,params.perspwidth,params.perspheight,params.missingcolour);
   return perspimage;
}

BITMAP4* convert(PARAMS params,BITMAP4* perspimage)
{
    int i,j,ai,aj,u,v,index;
    double x,y,r,phi,theta;
    RGB rgbsum,zero = {0,0,0};
    XYZ p,q;

    //starttime = GetRunTime();
	for (j=0;j<params.perspheight;j++) {
      for (i=0;i<params.perspwidth;i++) {
        	rgbsum = zero;

        	// Antialiasing loops, sub-pixel sampling
        	for (ai=0;ai<params.antialias;ai++) {
        	   x = i + ai / (double)params.antialias;
  	         for (aj=0;aj<params.antialias;aj++) {
     	         y = j + aj / (double)params.antialias;

					// Calculate vector to each pixel in the perspective image 
					CameraRay(x,y,&p);

					// Apply rotations in order
				   for (k=0;k<ntransform;k++) {
				      switch(transform[k].axis) {
				      case XTILT:
         				q.x =  p.x;
         				q.y =  p.y * transform[k].cvalue + p.z * transform[k].svalue;
         				q.z = -p.y * transform[k].svalue + p.z * transform[k].cvalue;
         				break;
      				case YROLL:
         				q.x =  p.x * transform[k].cvalue + p.z * transform[k].svalue;
         				q.y =  p.y;
         				q.z = -p.x * transform[k].svalue + p.z * transform[k].cvalue;
         				break;
      				case ZPAN:
         				q.x =  p.x * transform[k].cvalue + p.y * transform[k].svalue;
         				q.y = -p.x * transform[k].svalue + p.y * transform[k].cvalue;
         				q.z =  p.z;
         				break;
      				}
      				p = q;
   				}

					// Convert to fisheye image coordinates 
					theta = atan2(p.z,p.x);
					phi = atan2(sqrt(p.x * p.x + p.z * p.z),p.y);
					if (!params.rcorrection) {
						r = phi / params.fishfov; 
					} else {
					   r = phi * (params.a1 + phi * (params.a2 + phi * (params.a3 + phi * params.a4)));
      				if (phi > params.fishfov)
      				   r *= 10;
					}

					// Convert to fisheye texture coordinates 
					u = params.fishcenterx + r * params.fishradius * cos(theta);
					if (u < 0 || u >= params.fishwidth)
						continue;
					v = params.fishcentery + r * params.fishradiusy * sin(theta);
					if (v < 0 || v >= params.fishheight)
						continue;

					// Add up antialias contribution
					index = v * params.fishwidth + u;
					rgbsum.r += fishimage[index].r;
               rgbsum.g += fishimage[index].g;
               rgbsum.b += fishimage[index].b;
				}
			}

			// Set the pixel 
			index = j * params.perspwidth + i;
			perspimage[index].r = rgbsum.r / (params.antialias * params.antialias);
       	perspimage[index].g = rgbsum.g / (params.antialias * params.antialias);
     	 	perspimage[index].b = rgbsum.b / (params.antialias * params.antialias);

		}
	}
    return perspimage;
}


void write_file(PARAMS params, FILE * fptr, char fname[], char basename[], BITMAP4* perspimage)
{
    strcpy(fname,basename);
	if (params.imageformat == JPG) {
		strcat(fname,"_persp.jpg");
#ifdef ADDPNG
   } else if (params.imageformat == PNG) {
      strcat(fname,"_persp.png");
#endif
	} else {
		strcat(fname,"_persp.tga");
	}
	fptr = fopen(fname,"wb");
	if (params.imageformat == JPG) {
		JPEG_Write(fptr,perspimage,params.perspwidth,params.perspheight,100);
#ifdef ADDPNG
   } else if (params.imageformat == PNG) {
      PNG_Write(fptr,perspimage,params.perspwidth,params.perspheight,FALSE);
#endif
	} else {
   	Write_Bitmap(fptr,perspimage,params.perspwidth,params.perspheight,12);
	}
	fclose(fptr);
}

/*    
   Calculate the vector from the camera for a pixel
   We use a right hand coordinate system
   The camera FOV is the horizontal field of view
	The projection plane is as follows, one unit away.
     p1 +----------+ p4
        |          |
        |          |
        |          |
     p2 +----------+ p3
*/    
void CameraRay(double x,double y,XYZ *p)
{
   double h,v;
	double dh,dv;
	XYZ vp = {0,0,0},vd = {0,1,0}, vu = {0,0,1}; // Camera view position, direction, and up 
	XYZ right = {1,0,0};

	static XYZ p1,p2,p3,p4; // Corners of the view frustum
   static int first = TRUE;
   static XYZ deltah,deltav;
	static double inversew,inverseh;

   // Precompute what we can just once
   if (first) {
		dh = tan(params.perspfov / 2);
		dv = params.perspheight * dh / params.perspwidth;
      p1 = VectorSum(1.0,vp,1.0,vd,-dh,right, dv,vu);
      p2 = VectorSum(1.0,vp,1.0,vd,-dh,right,-dv,vu);
      p3 = VectorSum(1.0,vp,1.0,vd, dh,right,-dv,vu);
      p4 = VectorSum(1.0,vp,1.0,vd, dh,right, dv,vu);
      deltah.x = p4.x - p1.x;
      deltah.y = p4.y - p1.y;
      deltah.z = p4.z - p1.z;
      deltav.x = p2.x - p1.x;
      deltav.y = p2.y - p1.y;
      deltav.z = p2.z - p1.z;
		if (params.debug) {
			fprintf(stderr,"Projection plane\n");
			fprintf(stderr,"   angle: %g, distance: 1\n",params.perspfov*RTOD);
			fprintf(stderr,"   width: %g, height: %g \n",2*dh,2*dv);
			fprintf(stderr,"   p1: (%g,%g,%g)\n",p1.x,p1.y,p1.z);
         fprintf(stderr,"   p2: (%g,%g,%g)\n",p2.x,p2.y,p2.z);
         fprintf(stderr,"   p3: (%g,%g,%g)\n",p3.x,p3.y,p3.z);
         fprintf(stderr,"   p4: (%g,%g,%g)\n",p4.x,p4.y,p4.z);
		}
		inversew = 1.0 / params.perspwidth;
		inverseh = 1.0 / params.perspheight;
      first = FALSE;
   }

   h = x * inversew;
   v = (params.perspheight - 1 - y) * inverseh;
   p->x = p1.x + h * deltah.x + v * deltav.x;
   p->y = p1.y + h * deltah.y + v * deltav.y;
   p->z = p1.z + h * deltah.z + v * deltav.z;
}

/* 
   Sum 4 vectors each with a scaling factor
	Only used 4 times for the first pixel
*/ 
XYZ VectorSum(double d1,XYZ p1,double d2,XYZ p2,double d3,XYZ p3,double d4,XYZ p4)
{  
   XYZ sum;
   
   sum.x = d1 * p1.x + d2 * p2.x + d3 * p3.x + d4 * p4.x;
   sum.y = d1 * p1.y + d2 * p2.y + d3 * p3.y + d4 * p4.y;
   sum.z = d1 * p1.z + d2 * p2.z + d3 * p3.z + d4 * p4.z;
   
   return(sum); 
}  

void GiveUsage(char *s)
{
   fprintf(stderr,"Usage: %s [options] fisheyeimage\n",s);
   fprintf(stderr,"Options\n");
   fprintf(stderr,"   -w n        perspective image width, default = %d\n",params.perspwidth);
   fprintf(stderr,"   -h n        perspective image height, default = %d\n",params.perspheight);
   fprintf(stderr,"   -t n        field of view of perspective (degrees), default = %g\n",params.perspfov);
   fprintf(stderr,"   -s n        field of view of fisheye (degrees), default = %g\n",params.fishfov);
   fprintf(stderr,"   -c x y      center of the fisheye image, default is center of image\n");
	fprintf(stderr,"   -r n        fisheye radius (horizontal), default is half width of fisheye image\n");
	fprintf(stderr,"   -ry n       fisheye radius (vertical) for anamophic lens, default is circular fisheye\n");
	fprintf(stderr,"   -x n        tilt angle (degrees), default: 0\n");
   fprintf(stderr,"   -y n        roll angle (degrees), default: 0\n");
   fprintf(stderr,"   -z n        pan angle (degrees), default: 0\n");
   fprintf(stderr,"   -a n        antialiasing level, default = %d\n",params.antialias);
	fprintf(stderr,"   -f          create PGM files for ffmpeg remap filter, default: off\n");
   fprintf(stderr,"   -p n n n n  4th order lens correction, default: off\n");
	fprintf(stderr,"   -d          verbose mode, default: off\n");
}

/*
   Time scale at microsecond resolution but returned as seconds
	Machine / OS dependent, replace at will with other ms time call.
*/
double GetRunTime(void)
{
   double sec = 0;
   struct timeval tp;

   gettimeofday(&tp,NULL);
   sec = tp.tv_sec + tp.tv_usec / 1000000.0;

   return(sec);
}

void Normalise(XYZ *p)
{
   double length;

   length = p->x * p->x + p->y * p->y + p->z * p->z;
   if (length > 0) {
      length = sqrt(length);
      p->x /= length;
      p->y /= length;
      p->z /= length;
   } else {
      p->x = 0;
      p->y = 0;
      p->z = 0;
   }
}

void Init(void)
{
	params.fishfov         = 180;
	params.fishcenterx     = -1;
	params.fishcentery     = -1;
	params.fishradius      = -1;
	params.fishradiusy     = -1;
	params.antialias       = 2;
	params.remap           = FALSE;
	params.perspwidth      = 1600;
	params.perspheight     = 1200;
	params.perspfov        = 100;
	params.imageformat     = TGA;
   params.rcorrection     = FALSE;
   params.a1              = 1;
   params.a2              = 0;
   params.a3              = 0;
   params.a4              = 0;
	params.missingcolour.r = 128;
   params.missingcolour.g = 128;
   params.missingcolour.b = 128;
   params.missingcolour.a = 0;
	params.debug           = FALSE;
}

/*
   Create ffmpeg remap filter PGM file
   Two files, one for x coordinate and one for y coordinate
   https://trac.ffmpeg.org/wiki/RemapFilter
*/
void MakeRemap(char *bn)
{
   int i,j,k,ix,iy,u,v;
   char fname[256];
   FILE *fptrx = NULL,*fptry = NULL;
	double r,phi,theta;
	XYZ p,q;

   //sprintf(fname,"%s_x.pgm",bn);
	sprintf(fname,"fish2persp_x.pgm");
   fptrx = fopen(fname,"w");
   fprintf(fptrx,"P2\n%d %d\n65535\n",params.perspwidth,params.perspheight);

   //sprintf(fname,"%s_y.pgm",bn);
	sprintf(fname,"fish2persp_y.pgm");
   fptry = fopen(fname,"w");
   fprintf(fptry,"P2\n%d %d\n65535\n",params.perspwidth,params.perspheight);

   for (j=params.perspheight-1;j>=0;j--) {
      for (i=0;i<params.perspwidth;i++) {
			ix = -1;
			iy = -1;

			// Camera ray
         CameraRay((double)i,(double)j,&p);

			// Apply rotations
         for (k=0;k<ntransform;k++) {
            switch(transform[k].axis) {
            case XTILT:
               q.x =  p.x;
               q.y =  p.y * transform[k].cvalue + p.z * transform[k].svalue;
               q.z = -p.y * transform[k].svalue + p.z * transform[k].cvalue;
               break;
            case YROLL:
               q.x =  p.x * transform[k].cvalue + p.z * transform[k].svalue;
               q.y =  p.y;
               q.z = -p.x * transform[k].svalue + p.z * transform[k].cvalue;
               break;
            case ZPAN:
               q.x =  p.x * transform[k].cvalue + p.y * transform[k].svalue;
               q.y = -p.x * transform[k].svalue + p.y * transform[k].cvalue;
               q.z =  p.z;
               break;
            }
            p = q;
         }

         // Convert to fisheye image coordinates
         theta = atan2(p.z,p.x);
         phi = atan2(sqrt(p.x * p.x + p.z * p.z),p.y);
         if (!params.rcorrection) {
            r = phi / params.fishfov;
         } else {
            r = phi * (params.a1 + phi * (params.a2 + phi * (params.a3 + phi * params.a4)));
            if (phi > params.fishfov)
               r *= 10;
         }

         // Convert to fisheye texture coordinates
         u = params.fishcenterx + r * params.fishradius * cos(theta);
         v = params.fishcentery + r * params.fishradiusy * sin(theta);

         if (u >= 0 && v >= 0 && u < params.fishwidth && v < params.fishheight) {
            ix = u;
            iy = params.fishheight-1-v;
         }
         fprintf(fptrx,"%d ",ix);
         fprintf(fptry,"%d ",iy);
      }
      fprintf(fptrx,"\n");
      fprintf(fptry,"\n");
   }
   fclose(fptrx);
   fclose(fptry);
}

