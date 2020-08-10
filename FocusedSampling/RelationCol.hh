#ifndef RELGEN_RELATION_HH
#define RELGEN_RELATION_HH

#include "infra/glob_infra_standard_includes.hh"
#include "relspec.hh"
#include <unordered_set>
#include <unordered_map>

class RelationCol {
  public:
    typedef uint_vt col_t;
    typedef std::vector<col_t> col_vt;
    typedef std::unordered_set<uint> uint_st;

  public:
    RelationCol();
    RelationCol(const uint aNoAttr);
    RelationCol(const uint aNoAttr, const uint aCard);
    RelationCol(const relspec_t& aRelSpec, rng32_t& aRng);
    RelationCol(const RelationCol& R, const between_t& aPred); // selection

  public:
    inline uint card() const { return _card; }
    inline uint noAttr() const { return _cols.size(); }
    inline uint  val(const uint aRowId, const uint aAttrNo) const { return col(aAttrNo)[aRowId]; }
    inline uint& val_nc(const uint aRowId, const uint aAttrNo) { return col_nc(aAttrNo)[aRowId]; }
    inline const col_t& col(const uint i) const { return _cols[i]; }
    inline       col_t& col_nc(const uint i) { return _cols[i]; }
    inline const attrstat_t& attrstat(const uint i) const { return _attrstats[i]; }
    inline uint  min(const uint i) const { return _attrstats[i].min(); }
    inline uint  max(const uint i) const { return _attrstats[i].max(); }
  public:
    // init methods also init column statistics 
    void init(const relspec_t& aRelSpec, rng32_t& aRng);
    void init_col(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng);
    void init_col_key(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng);
    void init_col_div(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng);
    void init_col_general(const uint aAttrNo, const attrspec_t& aAttrSpec, rng32_t& aRng);
  public:
    void sample_of(const RelationCol& R, const uint aNoSamples, rng32_t& aRng);
    void sample_w_query(const RelationCol& R, uint_vt randVec, const query_t& query);
  public:
    void select(const RelationCol& R, const between_t&  aPred, const bool aWithNoDv = true);
    void apply_select(const between_t&  aPred, const bool aWithNoDv = true);
  public:
    bool qualifies(const uint aRowNo, const between_t&  aPred, bool opt = false, u_int idx = 0) const;
    bool qualifies(const uint aRowNo, const between_vt & aPred, uint_vt& resVec, bool opt = false);
    bool qualifies(const uint aRowNo, const between_vt& aPred, bool opt = false) const;
  public:
    void runstats(const bool aWithNoDv = true);
    void runstats_col(const uint aAttrNo, const bool aWithNoDv = true);
    uint col_min(const uint aAttrNo) const;
    uint col_max(const uint aAttrNo) const;
    uint col_nodv(const uint aAttrNo) const;
    void get_attr_stat(attrstat_t& aStat, const uint aAttrNo) const;
    void get_rel_stat(relstat_t& aStat) const;
  public:
    uint select_count(const between_t& aPred) const;
    uint select_count(const between_vt& aPred, bool opt = false) const;
    uint select_count(const between_vt& aPred, const uint_vt& tids, bool opt = false) const;
  public:
    void resize_cols(const uint aCard);
    void resize_attr_cols(const uint aNoAttr, const uint aCard);
    void copy_row_from(const uint aIdxTo, const RelationCol& R, const uint aIdxFrom);
    void copy_row_from(const uint aIdxTo, const RelationCol& R, const uint aIdxFrom, const query_t& query);
public:
    bool equal(const RelationCol& R) const;
  public:
    void write(std::ostream& os) const;
    void read(std::istream& os, const bool aWithNoDv);
  public:
    std::ostream& print(std::ostream& os, const int aWidth) const;
    std::ostream& print(std::ostream& os, const int aWidth, const std::string& aSep, const std::string& aLineEnd) const;
    std::ostream& print_attr_stat(std::ostream& os, const int aWidth) const;
    std::ostream& print_csv(std::ostream& os, const std::string& aSep) const;
  private:
    uint        _card;
    col_vt      _cols; 
    attrstat_vt _attrstats;

};
typedef std::vector<RelationCol> relcol_vt;
typedef std::vector<relcol_vt> relcol_vvt;

#endif

