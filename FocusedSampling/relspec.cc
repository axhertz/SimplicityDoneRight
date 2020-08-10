#include "relspec.hh"

/*
 * attrspec_t
 */

std::ostream&
attrspec_t::print(std::ostream& os) const {
  os << _attrName << ' '
     << distName() << ' '
     << max() << ' ';
  return os;
}

std::ostream&
operator<<(std::ostream& os, const attrspec_t& x) {
  return x.print(os);
}

/*
 * relspec_t
 */

int
relspec_t::getAttrNo(const char aAttrName) const {
  int lRes = -1;
  for(uint i = 0; i < noAttr(); ++i) {
    if(attrName(i) == aAttrName) {
      lRes = i;
      break;
    }
  }
  return lRes;
}

bool
relspec_t::push_back(const attrspec_t& aAttrSpec) {
  for(uint i = 0; i < noAttr(); ++i) {
    if(attrName(i) == aAttrSpec.attrName()) {
      return false;
    }
  }
  _attrspecs.push_back(aAttrSpec);
  return true;
}

std::ostream&
relspec_t::print(std::ostream& os) const {
  os << std::setw(1);
  os << _relName << ' ' << _card << ' ' << _attrspecs;
  return os;
}

std::ostream&
operator<<(std::ostream& os, const relspec_t& x) {
  return x.print(os);
}

/*
 *   stats
 */

std::ostream&
attrstat_t::print(std::ostream& os, const std::string& aSep) const {
  os << min() << aSep << max() << aSep << nodv();
  return os;
}

std::ostream&
relstat_t::print(std::ostream& os, const std::string& aSep) const {
  os << card();
  for(uint i = 0; i < _attrstats.size(); ++i) {
    os << aSep;
    _attrstats[i].print(os, aSep);
  }
  return os;
}

std::ostream& 
operator<<(std::ostream& os, const relstat_t& x) {
  return x.print(os, "|");
}

/*
 * between_t
 */

bool
between_t::set_attr_no(const relspec_t& aRelSpec) {
  int lAttrNo = aRelSpec.getAttrNo(attrName());
  if(0 <= lAttrNo) {
    _attrNo = lAttrNo;
  }
  return (0 <= lAttrNo);
}

bool
between_t::read(std::istream& aIs) {
  aIs >> _attrName;
  if(aIs.eof()) { return false; }
  aIs >> _attrNo;
  if(aIs.eof()) { return false; }
  aIs >> _lb;
  if(aIs.eof()) { return false; }
  aIs >> _ub;
  if(aIs.eof()) { return false; }
  return true;
}

std::ostream&
between_t::print(std::ostream& os, const bool aWithAttrNo) const {
  os << attrName() << ' ';
  if(aWithAttrNo) {
    os << attrNo() << ' ';
  }
  os << lb() << ' ' << ub();
  return os;
}

std::ostream&
operator<<(std::ostream& os, const between_t& x) {
  // os << x.attrName() << ' ' << x.lb() << ' ' << x.ub();
  // return os;
  return x.print(os, true);
}

bool
query_t::read(std::istream& aIs) {
  aIs >> _relname;
  if(aIs.eof()) { return false; }
  aIs >> _qno;
  if(aIs.eof()) { return false; }
  aIs >> _rescard;
  if(aIs.eof()) { return false; }
  if(0 >= rescard()) { return false; }
  uint lNoPreds = 0;
  aIs >> lNoPreds;
  if(aIs.eof()) { return false; }
  if(0 >= lNoPreds) { return false; }
  _preds.resize(lNoPreds);
  for(uint i = 0; i < lNoPreds; ++i) {
    if(!_preds[i].read(aIs)) {
      return false;
    }
  }
  return true;
}

std::ostream&
query_t::print(std::ostream& os) const {
  os << relname() << ' '
     << qno() << ' '
     << rescard() << ' '
     << no_preds() << ' '
     << preds();
  return os;
}


