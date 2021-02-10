#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>
#include "bitmaplib.h"

typedef struct {
   double x,y,z;
} XYZ;

typedef struct {
   int r,g,b;
} RGB;

typedef struct {
   int axis;
   double value;
   double cvalue,svalue;
} TRANSFORM;

typedef struct {
	double fishfov;      // Field of view
	int fishheight;      // Dimensions of fisheye image
	int fishwidth;
	int fishcenterx;     // Center of fisheye circle
	int fishcentery;
	int fishradius;      // Radius (horizontal) of the fisheye circle
	int fishradiusy;     // Vertical radius, deals with anamorphic lenses
	int antialias;       // Supersampling antialiasing
	int remap;           // Whether to create remap filters
	int perspwidth;      // Output dimensions
	int perspheight;
	double perspfov;     // Horizontal fov of perspective camera
	int imageformat;     // TGA, JPG ....
	int rcorrection;     // Apply tru-theta lens correction or not
	double a1,a2,a3,a4;  // Tru-theta lens correction parameters
	BITMAP4 missingcolour;
	int debug;
} PARAMS;

#define XTILT 0 
#define YROLL 1 
#define ZPAN  2 

#define ABS(x) (x < 0 ? -(x) : (x))
#define MIN(x,y) (x < y ? x : y)
#define MAX(x,y) (x > y ? x : y)
#define SIGN(x) (x < 0 ? (-1) : 1)
#define MODULUS(p) (sqrt(p.x*p.x + p.y*p.y + p.z*p.z))

// Prototypes
XYZ CameraRay(double,double,XYZ *, PARAMS);
XYZ VectorSum(double,XYZ,double,XYZ,double,XYZ,double,XYZ);
void GiveUsage(char *,PARAMS);
double GetRunTime(void);
void Normalise(XYZ *);
void Init(PARAMS);
void MakeRemap(char *,PARAMS, TRANSFORM*,int);
TRANSFORM* transforming(TRANSFORM*,int);
BITMAP4* open_fish_image(PARAMS,char*,BITMAP4*);
BITMAP4* create_persp_image(BITMAP4*,PARAMS);
BITMAP4* convert(PARAMS,BITMAP4*,BITMAP4*, TRANSFORM*,int);
void write_file(PARAMS,char*,char*,BITMAP4*);
void debug_info(PARAMS, TRANSFORM*,int);
PARAMS params_check(PARAMS);
TRANSFORM* create_transform(int,int,int,int);
void free_memory(BITMAP4*,BITMAP4*,TRANSFORM*);