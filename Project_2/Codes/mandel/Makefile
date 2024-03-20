CC     ?= gcc
CFLAGS  = -O3 -fopenmp -I.
LDFLAGS = -O3 -fopenmp -L. -lpng

.PHONY: all clean

all: mandel_omp mandel_seq

mandel_omp: mandel_omp.o pngwriter.o walltime.o
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

mandel_omp.o: mandel_omp.c consts.h pngwriter.h walltime.h
	$(CC) -c $(CFLAGS) $<

mandel_seq: mandel_seq.o pngwriter.o walltime.o
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

mandel_seq.o: mandel_seq.c consts.h pngwriter.h walltime.h
	$(CC) -c $(CFLAGS) $<

pngwriter.o: pngwriter.c pngwriter.h
	$(CC) -c $(CFLAGS) $<

walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $<

clean:
	$(RM) *.o mandel_omp mandel_seq
