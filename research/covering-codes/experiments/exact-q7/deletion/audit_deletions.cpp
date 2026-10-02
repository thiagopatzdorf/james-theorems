// Exhaustive radius-ball multiplicity audit, original code unmodified.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>
#include <chrono>
#include <stdexcept>
constexpr uint32_t N=40353607,V=182791;
std::vector<uint16_t> counts(N),owner(N);
std::array<uint32_t,9> powers;
std::array<int,9> current;
uint16_t center;
uint32_t perball;
void ball(int coordinate,int remaining,uint32_t id){
 if(coordinate==9){++counts[id];owner[id]=center;++perball;return;}
 ball(coordinate+1,remaining,id+current[coordinate]*powers[coordinate]);
 if(remaining)for(int digit=0;digit<7;++digit)if(digit!=current[coordinate])ball(coordinate+1,remaining-1,id+digit*powers[coordinate]);
}
std::string decode(uint32_t id){std::string s(9,'0');for(int j=8;j>=0;--j){s[j]='0'+id%7;id/=7;}return s;}
int main(int argc,char**argv){try{
 if(argc!=2)throw std::runtime_error("usage: audit_deletions code.txt");
 auto start=std::chrono::steady_clock::now();powers[8]=1;for(int i=7;i>=0;--i)powers[i]=powers[i+1]*7;
 std::ifstream f(argv[1],std::ios::binary);std::string line;std::vector<std::string> code;
 while(std::getline(f,line)){if(line.size()!=9||line.find_first_not_of("0123456")!=std::string::npos)throw std::runtime_error("invalid line");code.push_back(line);}
 if(code.size()!=1344)throw std::runtime_error("expected1344");auto sorted=code;std::sort(sorted.begin(),sorted.end());if(std::adjacent_find(sorted.begin(),sorted.end())!=sorted.end())throw std::runtime_error("duplicates");
 for(size_t k=0;k<code.size();++k){center=k;for(int j=0;j<9;++j)current[j]=code[k][j]-'0';perball=0;ball(0,4,0);if(perball!=V)throw std::runtime_error("ball volume mismatch");}
 std::vector<uint64_t> privatecounts(code.size(),0);std::vector<uint32_t> first(code.size(),UINT32_MAX);uint64_t uncovered=0,sum=0;uint16_t maxcount=0;
 for(uint32_t id=0;id<N;++id){sum+=counts[id];maxcount=std::max(maxcount,counts[id]);if(!counts[id])++uncovered;if(counts[id]==1){auto k=owner[id];++privatecounts[k];if(first[k]==UINT32_MAX)first[k]=id;}}
 if(sum!=uint64_t(code.size())*V)throw std::runtime_error("total multiplicity mismatch");
 std::cout<<"{\"ambient_words\":"<<N<<",\"M\":"<<code.size()<<",\"ball_volume\":"<<V<<",\"uncovered\":"<<uncovered<<",\"sum_coverage_multiplicities\":"<<sum<<",\"maximum_multiplicity\":"<<maxcount<<",\"runtime_seconds\":"<<std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()<<",\"words\":[";
 for(size_t k=0;k<code.size();++k){if(k)std::cout<<",";std::cout<<"{\"index\":"<<k<<",\"private_points\":"<<privatecounts[k]<<",\"first_private\":";if(first[k]==UINT32_MAX)std::cout<<"null";else std::cout<<"\""<<decode(first[k])<<"\"";std::cout<<"}";}std::cout<<"]}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<"\n";return 1;}}
