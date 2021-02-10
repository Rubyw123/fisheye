CC = gcc
CFLAGS = -Wall -O3
INCLUDES = 
LFLAGS = 
LIBS = -ljpeg -lm
FPIC = -fPIC
SHARE = -shared

OBJS = bitmaplib.o fish2persp.o 

all: libfish.so

libfish.so: $(OBJS)
	$(CC) $(SHARE) $(INCLUDES) $(CFLAGS) -o libfish.so $(OBJS) $(LFLAGS) $(LIBS)

fish2persp.o: fish2persp.c fish2persp.h
	$(CC) $(FPIC) $(INCLUDES) $(CFLAGS) -c fish2persp.c

bitmaplib.o: bitmaplib.c bitmaplib.h
	$(CC) $(FPIC) $(INCLUDES) $(CFLAGS) -c bitmaplib.c

clean:
	rm -rf core fish2persp *.o

