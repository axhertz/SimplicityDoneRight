#include "RelationCol.hh"
#include <algorithm>


RelationCol::RelationCol() : _card(0), _cols(), _attrstats() {}

RelationCol::RelationCol(const uint aNoAttr)
            : _card(0), _cols(aNoAttr), _attrstats(aNoAttr) {}

RelationCol::RelationCol(const uint aNoAttr, const uint aCard)
            : _card(aCard), _cols(aNoAttr), _attrstats(aNoAttr) {
  resize_cols(aCard);
}

RelationCol::RelationCol(const relspec_t& aRelSpec, rng32_t& aRng)
            : _card(0), _cols(), _attrstats() {
  init(aRelSpec, aRng);
}

RelationCol::RelationCol(const RelationCol& R, const between_t& aPred) 
            : _card(0), _cols(), _attrstats() {
  select(R, aPred);
}


void
RelationCol::init(const relspec_t& aRelSpec, rng32_t& aRng) {
  _card = aRelSpec.card();
  _cols.resize(aRelSpec.noAttr());
  _attrstats.resize(aRelSpec.noAttr());
  for(uint i = 0; i < aRelSpec.noAttr(); ++i) {
    col_nc(i).resize(card());
    init_col(i, aRelSpec.attrSpec(i), aRng);
  }
}


void
RelationCol::init_col(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng) {
  if(GenRandIntVec::kKey == aAttrSpec.dist()) {
    init_col_key(aAttrNo, aAttrSpec, aRng);
  } else
  if(GenRandIntVec::kDiv == aAttrSpec.dist()) {
    init_col_div(aAttrNo, aAttrSpec, aRng);
  } else {
    init_col_general(aAttrNo, aAttrSpec, aRng);
  }
}

void
RelationCol::init_col_key(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng) {
  GenRandIntVec lGriv;
  lGriv.generate(col_nc(aAttrNo), card(), aAttrSpec.spec(), aRng);
  _attrstats[aAttrNo]._min = 0;
  _attrstats[aAttrNo]._max = card() - 1;
  _attrstats[aAttrNo]._nodv = card();
}

void
RelationCol::init_col_div(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng) {
  GenRandIntVec lGriv;
  lGriv.generate(col_nc(aAttrNo), card(), aAttrSpec.spec(), aRng);
  _attrstats[aAttrNo]._min = 0;
  _attrstats[aAttrNo]._max = card() / aAttrSpec.div();
  _attrstats[aAttrNo]._nodv = (card() / aAttrSpec.div()) + 1;
}

void
RelationCol::init_col_general(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng) {
  GenRandIntVec lGriv;
  lGriv.generate(col_nc(aAttrNo), card(), aAttrSpec.spec(), aRng);
  runstats_col(aAttrNo);
}



void
RelationCol::sample_w_query(const RelationCol &R, uint_vt  randVec, const query_t& query) {
    _attrstats.resize(query.no_preds());
    _cols.resize(query.no_preds());
    resize_cols(randVec.size());

    for(uint i = 0; i < randVec.size(); ++i) {
        copy_row_from(i, R, randVec[i], query);
    }

    _card = randVec.size();
}

void
RelationCol::sample_of(const RelationCol& R, const uint aNoSamples, rng32_t& aRng) {
  _attrstats.resize(R.noAttr());
  _cols.resize(R.noAttr());
  resize_cols(aNoSamples);

  if(10 * aNoSamples < R.card()) {
    uint_st lRidSet(aNoSamples);
    uint lRowCount = 0;
    while(lRidSet.size() < aNoSamples) {
      const uint lRid = aRng() % R.card();
      if(lRidSet.end() == lRidSet.find(lRid)) {
        copy_row_from(lRowCount, R, lRid);
        ++lRowCount;
        lRidSet.insert(lRid);
      }
    }
  } else {
    uint_vt lRidVec(R.card());
    for(uint i = 0; i < R.card(); ++i) {
      lRidVec[i] = i;
    }
    GenRandIntVec::vec_permute(lRidVec, aRng);
    for(uint i = 0; i < aNoSamples; ++i) {
      copy_row_from(i, R, lRidVec[i]);
    }
  }
  _card = aNoSamples;
  runstats();
}


void
RelationCol::select(const RelationCol& R, const between_t& aPred, const bool aWithNoDv) {
  const uint lNoAttr = R.noAttr();
  const uint lCard   = R.select_count(aPred);
  _card = lCard;
  _cols.resize(lNoAttr);
  _attrstats.resize(lNoAttr);
  for(uint i = 0; i < lNoAttr; ++i) {
    col_nc(i).resize(card());
  }

  const col_t& lCol = R.col(aPred.attrNo());
  uint k = 0;
  for(uint i = 0; i < R.card(); ++i) {
    if(aPred(lCol[i])) {
      for(uint j = 0; j < lNoAttr; ++j) {
        col_nc(j)[k] = R.col(j)[i];
      }
      ++k;
    }
  }
  runstats(aWithNoDv);
}

void
RelationCol::apply_select(const between_t& aPred, const bool aWithNoDv) {
  uint lLast = card() - 1;
  uint lNoQualify = 0; // walking from 0..card()-1 at most
  while(lNoQualify <= lLast) {
    if(qualifies(lNoQualify, aPred)) {
      ++lNoQualify;
    } else {
      if(lNoQualify < lLast) {
        copy_row_from(lNoQualify, (*this), lLast);
        --lLast;
      } else {
        break;
      }
    }
  }
  for(uint i = 0; i < noAttr(); ++i) {
    col_nc(i).resize(lNoQualify);
  }
  _card = lNoQualify;
  runstats(aWithNoDv); 
}


bool
RelationCol::qualifies(const uint aRowNo, const between_t& aPred, bool opt, u_int idx) const {
    if (opt) {
        return aPred.qualifies(val(aRowNo, idx));
    }
    return aPred.qualifies(val(aRowNo, aPred.attrNo()));
    }


//focused sampling for greedy enumeration
bool
RelationCol::qualifies(const uint aRowNo, const between_vt & aPred, uint_vt& resVec, bool opt){
    bool lQualifies = true;
    bool first_true = false;
    for(uint i = 0; (i < aPred.size()) && lQualifies; ++i) {
        lQualifies &= qualifies(aRowNo, aPred[i], opt, i);
        if (lQualifies && i == 0){
            first_true = true;
        }
    }
    if (first_true){
        for(uint j = 1; (j < aPred.size()); j++){
            resVec.push_back(qualifies(aRowNo, aPred[j], opt, j));
        }
    }
    return lQualifies;
}

bool
RelationCol::qualifies(const uint aRowNo, const between_vt& aPred, bool opt) const {
  bool lQualifies = true;
  for(uint i = 0; (i < aPred.size()) && lQualifies; ++i) {
    lQualifies &= qualifies(aRowNo, aPred[i], opt, i);
  }
  return lQualifies;
}

void
RelationCol::runstats(const bool aWithNoDv) {
  for(uint i = 0; i < noAttr(); ++i) {
    runstats_col(i, aWithNoDv);
  }
}

void
RelationCol::runstats_col(const uint aAttrNo, const bool aWithNoDv) {
  _attrstats[aAttrNo]._min  = col_min(aAttrNo);
  _attrstats[aAttrNo]._max  = col_max(aAttrNo);
  if(aWithNoDv) {
    _attrstats[aAttrNo]._nodv = col_nodv(aAttrNo);
  } else {
    _attrstats[aAttrNo]._nodv = 0;
  }
}

void 
RelationCol::get_attr_stat(attrstat_t& aStat, const uint aAttrNo) const {
  aStat = attrstat(aAttrNo);
}

void 
RelationCol::get_rel_stat(relstat_t& aStat) const {
  aStat._card = card();
  aStat._attrstats = _attrstats;
}

uint
RelationCol::col_min(const uint aAttrNo) const {
  uint lRes = std::numeric_limits<uint>::max();
  const col_t& lCol = col(aAttrNo);
  for(uint i = 0; i < card(); ++i) {
    if(lCol[i] < lRes) {
      lRes = lCol[i];
    }
  }
  return lRes;
}

uint
RelationCol::col_max(const uint aAttrNo) const {
  uint lRes = 0;
  const col_t& lCol = col(aAttrNo);
  for(uint i = 0; i < card(); ++i) {
    if(lCol[i] > lRes) {
      lRes = lCol[i];
    }
  }
  return lRes;
}

uint
RelationCol::col_nodv(const uint aAttrNo) const {
  const col_t& lCol = col(aAttrNo);
  uint_st lSet(std::max<uint>(10000, attrstat(aAttrNo).max()));
  for(uint i = 0; i < card(); ++i) {
    lSet.insert(lCol[i]);
  }
  return lSet.size();
}

uint
RelationCol::select_count(const between_t& aPred) const {
  uint lRes = 0;
  const col_t& lCol = col(aPred.attrNo());
  for(uint i = 0; i < card(); ++i) {
    lRes += aPred(lCol[i]);
  }
  return lRes;
}

uint
RelationCol::select_count(const between_vt& aPred, bool opt) const {
  uint lRes = 0;
  for(uint i = 0; i < card(); ++i) {
    lRes += qualifies(i, aPred, opt);
  }
  return lRes;
}

uint
RelationCol::select_count(const between_vt& aPred, const uint_vt& tids , bool opt) const {
    uint lRes = 0;
    for(uint i : tids) {
        lRes += qualifies(i, aPred, opt);
    }
    return lRes;
}




void
RelationCol::resize_cols(const uint aCard) {
  for(uint i = 0; i < noAttr(); ++i) {
    _cols[i].resize(aCard);
  }
}

void
RelationCol::resize_attr_cols(const uint aNoAttr, const uint aCard) {
  _card = aCard;
  _cols.resize(aNoAttr);
  _attrstats.resize(aNoAttr);
  resize_cols(aCard);
  runstats();
}


void
RelationCol::copy_row_from(const uint aIdxTo, const RelationCol& R, const uint aIdxFrom) {
  for(uint i = 0; i < noAttr(); ++i) {
     col_nc(i)[aIdxTo] = R.col(i)[aIdxFrom];
  }
}

void
RelationCol::copy_row_from(const uint aIdxTo, const RelationCol& R, const uint aIdxFrom, const query_t& query) {
    for(uint i = 0; i < noAttr(); ++i) {
        col_nc(i)[aIdxTo] = R.col(query.preds()[i].attrNo())[aIdxFrom];
    }
}

bool
RelationCol::equal(const RelationCol& R) const {
  if(card() != R.card()) { return false; }
  if(noAttr() != R.noAttr()) { return false; }
  bool lRes = true;
  for(uint i = 0; (i < card()) && lRes; ++i) {
    for(uint j = 0; (j < noAttr()) && lRes; ++j) {
      lRes &= (val(i,j) == R.val(i,j));
    }
  }
  return lRes;
}

void
RelationCol::write(std::ostream& os) const {
  os << card() << ' ' << noAttr() << std::endl;
  for(uint i = 0; i < card(); ++i) {
    for(uint j = 0; j < noAttr(); ++j) {
      if(0 < j) {
        os << ' ';
      }
      os << val(i, j);
    }
    os << std::endl;
  }
}

void
RelationCol::read(std::istream& aIs, const bool aWithNoDv) {
  int lCard = 0;
  int lNoAttr = 0;
  aIs >> lCard >> lNoAttr;
  resize_attr_cols(lNoAttr, lCard);
  for(uint i = 0; i < card(); ++i) {
    for(uint j = 0; j < noAttr(); ++j) {
      aIs >> val_nc(i, j);
    }
  }
  runstats(aWithNoDv);
}

std::ostream&
RelationCol::print(std::ostream& os, const int w) const {
  for(uint i = 0; i < card(); ++i) {
    for(uint j = 0; j < noAttr(); ++j) {
      if(0 < j) {
        os << ' ';
      }
      // os << std::setw(w) << col(j)[i];
      os << std::setw(w) << val(i, j);
    }
    os << std::endl;
  }
  return os;
}

std::ostream&
RelationCol::print(std::ostream& os, const int w, const std::string& aSep, const std::string& aLineEnd) const {
  for(uint i = 0; i < card(); ++i) {
    for(uint j = 0; j < noAttr(); ++j) {
      if(0 < j) {
        os << aSep;
      }
      os << std::setw(w) << col(j)[i];
    }
    os << aLineEnd << std::endl;
  }
  return os;
}

std::ostream&
RelationCol::print_attr_stat(std::ostream& os, const int w) const {
  for(uint i = 0; i < noAttr(); ++i) {
    os << std::setw(w) << _attrstats[i]._min << ' ' 
       << std::setw(w) << _attrstats[i]._max << ' ' 
       << std::setw(w) << _attrstats[i]._nodv << std::endl;
  }
  return os;
}

std::ostream&
RelationCol::print_csv(std::ostream& os, const std::string& aSep) const {
  for(uint i = 0; i < card(); ++i) {
    for(uint j = 0; j < noAttr(); ++j) {
      if(0 < j) {
        os << aSep;
      }
      os << col(j)[i];
    }
    os << std::endl;
  }
  return os;
}

