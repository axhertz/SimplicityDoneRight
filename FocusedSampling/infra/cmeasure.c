#include "cmeasure.h"

#define NS   ((int64_t) 1000LL * 1000LL * 1000LL)
#define MUES ((int64_t) 1000LL * 1000LL)
#define MS   ((int64_t) 1000LL)

int
cmeasure_print_clock_resolution() {
  int lRc = 0;
  struct timespec lTx;
  lRc = clock_getres(CLOCK_REALTIME, &lTx);
  printf("resolution of CLOCK_REALTIME is ");
  if(0 != lTx.tv_sec) {
    printf("%ld s and ", lTx.tv_sec);
  }
  printf("%ld ns\n", lTx.tv_nsec);
  return lRc;
}

int
cmeasure_start(struct cmeasure_t* aMeasure) {
  int lRc = 0;
  lRc = clock_gettime(CLOCK_REALTIME, &(aMeasure->_begin));
  return lRc;
}
  
int
cmeasure_stop(struct cmeasure_t* aMeasure) {
  int lRc = 0;
  lRc = clock_gettime(CLOCK_REALTIME, &(aMeasure->_end));
  return lRc;
}

int64_t
cmeasure_total_ns(struct cmeasure_t* aMeasure) {
  int64_t lRes = 0;
  lRes  = (int64_t) (aMeasure->_end.tv_sec - aMeasure->_begin.tv_sec) * NS;
  lRes += (int64_t) (aMeasure->_end.tv_nsec - aMeasure->_begin.tv_nsec);
  return lRes;
}

double
cmeasure_total_ms(struct cmeasure_t* aMeasure) {
  return (((double) cmeasure_total_ns(aMeasure)) / ((double) 1000.0 * 1000.0));
}

double
cmeasure_total_s(struct cmeasure_t* aMeasure) {
  return (((double) cmeasure_total_ns(aMeasure)) / ((double) 1000.0 * 1000.0 * 1000.0));
}


double
cmeasure_div_ms(struct cmeasure_t* aMeasure, const double lDivBy) {
  double lTotTime = (double) cmeasure_total_ms(aMeasure);
  return (lTotTime / lDivBy);
}

double
cmeasure_div_ns(struct cmeasure_t* aMeasure, const double lDivBy) {
  double lTotTime = (double) cmeasure_total_ns(aMeasure);
  return (lTotTime / lDivBy);
}

int
cmeasure_print(struct cmeasure_t* aMeasure, const char* aFormatString) {
  int lRes = 0; // number of blanks missing 
  int64_t lTime = cmeasure_total_ns(aMeasure);
  if(NS < lTime) {
    double x = (double) lTime / (double) NS;
    printf(aFormatString, x);
    printf(" [s]");
    lRes = 3;
  } else
  if(MUES < lTime) {
    double x = (double) lTime / (double) MUES;
    printf(aFormatString, x);
    printf(" [ms]");
    lRes = 2;
  } else
  if(MS < lTime) {
    double x = (double) lTime / (double) MS;
    printf(aFormatString, x);
    printf(" [mues]");
    lRes = 0;
  } else {
    double x = (double) lTime;
    printf(aFormatString, x);
    printf(" [ns]");
    lRes = 2;
  }
  return lRes;
}


int
cmeasure_print_fin(struct cmeasure_t* aMeasure, const char* aFormatString, const char* aFinalString) {
  int lRes = cmeasure_print(aMeasure, aFormatString);
  if(0 != aFinalString) {
    printf("%s", aFinalString);
  }
  return lRes;
}


