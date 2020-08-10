#include "GenRandIntVec.hh"
#include <algorithm>

GenRandIntVec::GenRandIntVec() : _freq() {}


GenRandIntVec::dist_t
GenRandIntVec::str2dist(const std::string& aDist) {
  for(int i = 0; i < kNoDist; ++i) {
    if(_distname[i] == aDist) {
      return ((dist_t) i);
    }
  }
  return kNoDist;
}

const std::string&
GenRandIntVec::dist2str(const dist_t aDist) {
  return _distname[aDist < kNoDist ? aDist : kNoDist];
}

void 
GenRandIntVec::generate(uint_vt& aVec, const uint aCard, const param_t& aParam, rng32_t& aRng) {
  if(aVec.size() != aCard) {
    aVec.resize(aCard);
  }
  if(aParam.fill()) {
    assert((uint) aParam.max() <= aCard);
  }

  switch(aParam.dist()) {
    case kKey:  generate_key(aVec, aCard, aParam, aRng); break;
    case kDiv:  generate_div(aVec, aCard, aParam, aRng); break;
    default: assert(0 == 1);
  }
}

void 
GenRandIntVec::generate_key(uint_vt& aVec, const uint aCard, const param_t& aParam, rng32_t& aRng) {
  for(uint i = 0; i < aCard; ++i) {
    aVec[i] = i;
  }
  if(aParam.permute()) {
    vec_permute(aVec, aRng);
  } else
  if(aParam.sort()) {
    // is sorted already
  }
}

void 
GenRandIntVec::generate_div(uint_vt& aVec, const uint aCard, const param_t& aParam, rng32_t& aRng) {
  const uint d = aParam.div();
  for(uint i = 0; i < aCard; ++i) {
    aVec[i] = i / d;
  }
  if(aParam.permute()) {
    vec_permute(aVec, aRng);
  } else
  if(aParam.sort()) {
    // is sorted already
  }
}

void
GenRandIntVec::vec_sort(uint_vt& aVec) {
    std::sort(aVec.begin(), aVec.end());
}

void
GenRandIntVec::vec_permute(uint_vt& aVec, rng32_t& aRng) {
    for(size_t i = aVec.size() - 1; i > 0; --i) {
        std::swap(aVec[i], aVec[aRng() % i]);
    }
}



void
GenRandIntVec::vec_revsort(uint_vt& aVec) {
  std::sort(aVec.begin(), aVec.end(), std::greater<int>());
}
void
GenRandIntVec::freq_expand(uint_vt& aVecOut, const uint_vt& aFreqVec) {
  size_t k = 0;
  for(size_t i = 0; i < aFreqVec.size(); ++i) {
    for(uint j = 0; j < aFreqVec[i]; ++j) {
      aVecOut[k++] = i;
    }
  }
}


const GenRandIntVec::string_vt GenRandIntVec::_distname = {
  "key",
  "div",
  "uni",
  "exp",
  "norm",
  "zipf",
  "self",
  "pois",
  "<invalid_distribution>"
};
