#include "infra/glob_infra_standard_includes.hh"
#include "relspec.hh"
#include "RelationCol.hh"
//#include "arg.hh"
#include <fstream>
#include <chrono>
#include<iostream>
#include <unistd.h>
#include <random>
#include <algorithm>




#define GetCurrentDir getcwd


extern "C" {
  #include "infra/cmeasure.h"
}

// #define __MACOS


const std::string gDirRel   = "../data/table/";
const std::string gDirQuery = "../data/query/";


using namespace std;

const uint cardinality = 581012; // |forest data set|


uint_vt getRandVec(rng32_t aRng, uint sampleSize){
    uniform_int_distribution<int> dist {0, cardinality-1};
    auto gen = [&dist, &aRng](){
        return dist(aRng);
    };
    uint_vt randVec(sampleSize);
    generate(begin(randVec), end(randVec), gen);
    return  randVec;
}


std::string get_current_dir() {
    char buff[FILENAME_MAX]; //create string buffer to hold path
    GetCurrentDir( buff, FILENAME_MAX );
    std::string current_working_dir(buff);
    return current_working_dir;
}


void
gen_sample_for_query(relcol_vt& lSamples, const RelationCol& R, const uint_vt&  randVec,  const query_t& query) {
        lSamples.resize(randVec.size());
       lSamples[0].sample_w_query(R, randVec, query);
}

void
testSampleSizes(rng32_t& aRng, std::string tableName, const std::string& queryName,
        const std::string& samplingMethod, bool reuseTIDs){
    std::ofstream resultFile;
    std::cout<< "method: "<<samplingMethod << "\t reuse TIDs: "<< reuseTIDs << "\t query: " << queryName
    <<"\t result file: " << "../result/result.txt" <<std::endl;
    resultFile.open("../result/result.txt");
    RelationCol R;
    std::string lFilenameRel = gDirRel + tableName;
    std::string lFilenameQuery = gDirQuery + queryName;
    std::ifstream lIsRel(lFilenameRel);
    std::cout<<get_current_dir()<<"\n";

    if(!lIsRel) {
        std::cout << "can't open relation file '" << lFilenameRel << "'." << std::endl;
        return;
    }
    R.read(lIsRel, false);
    const uint n = R.card();
    uint max_sample_size = 11000;
    uint_vt randVecFull = getRandVec(aRng, max_sample_size);
    uint_vt randVec;

    for (uint i = 0; i < 100; i++){
        std::cout<<"run "<<i<<" of "<< 100<<endl;
        std::ifstream lIsQuery(lFilenameQuery);

        if(!lIsQuery) {
            std::cout << "can't open query file '" << lFilenameQuery << "'." << std::endl;
            return;
        }

        if (reuseTIDs) {
            randVec = uint_vt(randVecFull.begin(), randVecFull.begin() + 1000 + 100 * i);
        }

        uint lCount = 0;
        uint lCardCheck = 0;
        query_t lQuery;
        relcol_vt sampleForQuery;
        uint_vt  resVec;
        sampleForQuery.clear();
        auto t1 = std::chrono::high_resolution_clock::now();
        while(lQuery.read(lIsQuery) && (10000 > lCount)) {
            if (samplingMethod == "traditional") {
                if (!reuseTIDs) {
                    randVec = getRandVec(aRng, 1000 + i * 100);
                }
                gen_sample_for_query(sampleForQuery, R, randVec, lQuery);
                lCardCheck = sampleForQuery[0].select_count(lQuery.preds(), true);
            } else if (samplingMethod == "focused") {
                if (!reuseTIDs) {
                    randVec = getRandVec(aRng, 1000 + i * 100);
                }
                lCardCheck = R.select_count(lQuery.preds(), randVec, false);
            } else {std::cout<<"no valid sampling method given";}
            /*
            true cardinlity: lQuery._rescard
            estimated cardinality: static_cast<double>(lCardCheck) / randVec.size()* n
            */
            ++lCount;
            //std::cout<<"true "<<lQuery.rescard()<< " est " <<static_cast<double>(lCardCheck) / randVec.size()* n<<"\n";
        }
        auto t2 = std::chrono::high_resolution_clock::now();
        std::cout<<"eval took:" << std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count()<<"\n";
        resultFile<<i<<" "<<std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1).count()<<"\n";
        resultFile.flush();
        lIsQuery.close();
    }
    resultFile.close();
}


static void show_usage(const std::string& name)
{
    std::cout << "Usage: " << name << " <option(s)> SOURCES "
              << "Options:\n"
              << "\t-help, -h,\t show this help message\n"
              << "\t-n_preds,\t specify number of predicates [3|5|7]\n"
              << "\t-method,\t specify sampling_method [focused|traditional]\n"
              << "\t-reuse_tids,\t specify whether to reuse tids [0|1]\n"
              << "\t-enum_pred,\t specify whether to order predicates [0|1]\n"
              << "example:  -n_preds 7 -method focused -reuse_tids 1 -enum_pred 1 "
              << std::endl;
}

int main(int argc, char* argv[])
{

    std::vector <std::string> sources;
    std::string destination;
    bool reuse_tids = true;
    std::string method = "focused";
    std::string query_file = "query_frt_qu7";
    std::string enum_pred = "_enum.txt";

    if(argc < 9){
        show_usage(argv[0]);
        return 1;
    }
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if ((arg == "-h") || (arg == "-help")) {
            show_usage(argv[0]);
            return 0;
        }else if (arg == "-method") {
            if (i + 1 < argc) {
                destination = argv[++i];
                if (destination == "focused") { method = "focused"; }
                else if (destination == "traditional") { method = "traditional"; }
                else {
                    std::cerr << "-method option requires one argument {traditional; focused}." << std::endl;
                    return 1;
                }
             }
        }
        else if (arg == "-n_preds") {
            if (i + 1 < argc) {
                destination = argv[++i];
                if (destination == "3") { query_file = "query_frt_qu3"; }
                else if (destination == "5") { query_file = "query_frt_qu5"; }
                else if (destination == "7") { query_file = "query_frt_qu7"; }
                else {
                    std::cerr << "-n_preds option requires one argument."<< std::endl;
                    return 1;
                }
            }
        } else if (arg == "-reuse_tids") {
            if (i + 1 < argc) {
                destination = argv[++i];
                if (destination == "0") { reuse_tids = false; }
                else if (destination == "1") { reuse_tids = true; }
                else {
                    std::cerr << "-fixed_tids option requires one argument." << std::endl;
                    return 1;
                }
            }
        } else if (arg == "-enum_pred") {
            if (i + 1 < argc) {
                destination = argv[++i];
                if (destination == "0") { enum_pred = ".txt"; }
                else if (destination == "1") { enum_pred = "_enum.txt"; }
                else {
                    std::cerr << "-enum_pred option requires one argument." << std::endl;
                    return 1;
                }
            }
        }
        else {
            std::cerr<< "invalid arguments" << std::endl;
            show_usage(argv[0]);
            return 1;
        }
    }
    rng32_t lRng;
    testSampleSizes(lRng, "forest_data_normalised.csv", query_file+enum_pred, method, reuse_tids);

    return 0;
}

