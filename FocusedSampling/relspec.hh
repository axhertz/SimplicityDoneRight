#ifndef RELGEN_RELSPEC_HH
#define RELGEN_RELSPEC_HH

#include "infra/glob_infra_standard_includes.hh"
#include "infra/vector_ops.hh"
#include "infra/GenRandIntVec.hh"

#include <random>

/*
 *  contains
 *  attrspec_t to specify the generation of attribute values
 *  relspec_t  to specify the generation of a relation
 *  between_t  range predicate
 */


typedef GenRandIntVec::dist_t  dist_et;
typedef GenRandIntVec::param_t rndvecspec_t;

struct attrspec_t {
  char         _attrName;
  rndvecspec_t _spec;

  attrspec_t() : _attrName('X'), _spec() {}

  attrspec_t(const char aAttrName, const std::string& aDistName,
             const uint aMax)
            : _attrName(aAttrName),
              _spec(aDistName, aMax,  0, 0) {}

  attrspec_t(const char aAttrName, const std::string& aDistName,
             const uint aMax,  const double aParam,
             const uint aFlags, const int aOrder) 
            : _attrName(aAttrName),
              _spec(aDistName, aMax,   aFlags, aOrder) {}

  inline       char          attrName() const { return _attrName; }
  inline       void          attrName(const char c) { _attrName = c; }
  inline const rndvecspec_t& spec() const { return _spec; }
  inline       dist_et       dist() const { return spec().dist(); }
  inline const std::string&  distName() const { return _spec.name(); }
  inline       uint          max() const { return spec().max(); }
  inline       uint          mod() const { return spec().mod(); }
  inline       uint          div() const { return spec().div(); }



  std::ostream& print(std::ostream& os) const;
};

std::ostream& operator<<(std::ostream& os, const attrspec_t& x);

typedef std::vector<attrspec_t> attrspec_vt;

struct relspec_t {
  std::string  _relName;
  uint         _card;
  attrspec_vt  _attrspecs;
  relspec_t()
              : _relName(), _card(0), _attrspecs() {}
  relspec_t(const std::string& aName, const uint aCard)
              : _relName(aName), _card(aCard), _attrspecs() {}
  relspec_t(const std::string& aName, const uint aCard, const attrspec_vt& aAttrSpecs)
              : _relName(aName), _card(aCard), _attrspecs(aAttrSpecs) {}

  inline const std::string& relName() const { return _relName; }
  inline uint card() const { return _card; }
  inline void card(const uint aCard) { _card = aCard; }
  inline uint noAttrSpecs() const { return _attrspecs.size(); }
  inline uint noAttr() const { return _attrspecs.size(); }
  inline const attrspec_t&  attrSpec(const uint i) const { return _attrspecs[i]; }
  inline       attrspec_vt& attrSpecsNC() { return _attrspecs; }
  inline       char         attrName(const uint i) const { return _attrspecs[i]._attrName; }
               int          getAttrNo(const char aAttrName) const;
  inline       int          max  (const uint i) const { return _attrspecs[i].max()  ; }
               bool         push_back(const attrspec_t& aAttrSpec);
  std::ostream& print(std::ostream& os) const;
};

std::ostream& operator<<(std::ostream& os, const relspec_t& x);

struct attrstat_t {
  uint _min;
  uint _max;
  uint _nodv;
  inline  uint min() const { return _min; }
  inline  uint max() const { return _max; }
  inline  uint nodv() const { return _nodv; }
  std::ostream& print(std::ostream& os, const std::string& aSep) const;
};
typedef std::vector<attrstat_t> attrstat_vt;

struct relstat_t {
  uint        _card;
  attrstat_vt _attrstats;
  relstat_t() : _card(0), _attrstats() {}
  inline uint card() const { return _card; }
  std::ostream& print(std::ostream& os, const std::string& aSep) const;
};

std::ostream& operator<<(std::ostream& os, const relstat_t&);

struct between_t {
  char _attrName;
  uint _attrNo;
  uint _lb;
  uint _ub;
  between_t() : _attrName('X'), _attrNo(-1), _lb(0), _ub(0) {}
  between_t(const char aAttrName, const uint aAttrNo, const uint aLb, const uint aUb)
           : _attrName(aAttrName), _attrNo(aAttrNo), _lb(aLb), _ub(aUb) {}
  inline char attrName() const { return _attrName; }
  inline uint attrNo() const { return _attrNo; }
  inline uint  lb() const { return _lb; }
  inline uint  ub() const { return _ub; }
  inline void  lb(const uint aLb) { _lb = aLb; }
  inline void  ub(const uint aUb) { _ub = aUb; }
  inline bool qualifies(const uint aVal) const;
  inline bool operator()(const int& aVal) const { return qualifies(aVal); }
         bool set_attr_no(const relspec_t& aRelSpec);
  inline void set_attr_no(const uint aAttrNo) { _attrNo = aAttrNo; }
  inline void set_attr_name(const char aAttrName) { _attrName = aAttrName; }
  bool read(std::istream& os);
  std::ostream& print(std::ostream& os, const bool aWithAttrNo = false) const;
};

bool
between_t::qualifies(const uint aVal) const {
  return ((lb() <= aVal) && (aVal <= ub()));
}

std::ostream&
operator<<(std::ostream& os, const between_t&);

typedef std::vector<between_t> between_vt;


struct query_t {
  std::string _relname;
  uint        _qno;
  uint        _rescard;
  between_vt  _preds;
  query_t() : _relname(), _qno(0), _rescard(0), _preds() {}
  inline const  std::string& relname() const { return _relname; }
  inline void                relname(const std::string& aRelName) { _relname = aRelName; }
  inline        uint         qno() const { return _qno; }
  inline        void         qno(const uint aQNo) { _qno = aQNo; }
  inline        uint         rescard() const { return _rescard; }
  inline        void         rescard(const uint aResCard) { _rescard = aResCard; }
  inline        uint         no_preds() const { return _preds.size(); }
  inline        void         no_preds(const uint aNoPreds) { _preds.resize(aNoPreds); }
  inline const  between_vt&  preds() const { return _preds; }
  inline        between_vt&  preds_nc() { return _preds; }
  inline const  between_t&   pred(const uint i) const { return _preds[i]; }
  inline void set_attr_name(const uint i, const char aAttrName) { _preds[i].set_attr_name(aAttrName); }
  inline void set_attr_no(const uint i, const uint aAttrNo) { _preds[i].set_attr_no(aAttrNo); }
  bool          read(std::istream& aIs);
  std::ostream& print(std::ostream& os) const;
};

#endif
