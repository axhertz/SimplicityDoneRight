#ifndef CMEASURE_H
#define CMEASURE_H

#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <stdio.h>
#include <time.h>
#include <inttypes.h>

#ifdef __linux__
// #include <bits/types/struct_timespec.h>
#endif

struct cmeasure_t {
  struct timespec _begin;
  struct timespec _end;
};

int     cmeasure_print_clock_resolution();
int     cmeasure_start(struct cmeasure_t* aMeasure);
int     cmeasure_stop(struct cmeasure_t* aMeasure);
int64_t cmeasure_total_ns(struct cmeasure_t* aMeasure);
double  cmeasure_total_ms(struct cmeasure_t* aMeasure);
double  cmeasure_total_s(struct cmeasure_t* aMeasure);
double  cmeasure_div_ms(struct cmeasure_t* aMeasure, const double lDivBy);
double  cmeasure_div_ns(struct cmeasure_t* aMeasure, const double lDivBy);
int     cmeasure_print(struct cmeasure_t* aMeasure, const char* aFormatString);
int     cmeasure_print_fin(struct cmeasure_t* aMeasure, const char* aFormatString, const char* aFinalString);

#endif

