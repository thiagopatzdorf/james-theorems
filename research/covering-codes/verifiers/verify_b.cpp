// Independent verifier: multi-source BFS on the Hamming graph.
// Graph distance equals Hamming distance; each edge changes one coordinate.
#include <openssl/sha.h>
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <iterator>
#include <limits>
#include <set>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc, char** argv) {
 try {
  if(argc!=5) throw std::runtime_error("usage: verify_b q n R code.txt");
  auto start=std::chrono::steady_clock::now();
  auto number=[](const char* s) {std::string v(s);size_t k=0;int a=std::stoi(v,&k);
   if(k!=v.size()) throw std::runtime_error("bad integer");return a;};
  int q=number(argv[1]),n=number(argv[2]),R=number(argv[3]);
  if(q<2||q>10||n<1||n>32||R<0||R>n) throw std::runtime_error("parameter range");
  uint64_t N=1;std::vector<uint64_t> power(n);
  // Text coordinate zero is most significant; no modulo alphabet reduction.
  for(int i=n-1;i>=0;--i) {
   power[i]=N;
   if(N>std::numeric_limits<uint32_t>::max()/uint64_t(q))
    throw std::runtime_error("uint32 universe overflow");
   N*=q;
  }
  if(N>250000000) throw std::runtime_error("memory guard");
  std::ifstream in(argv[4],std::ios::binary);
  if(!in) throw std::runtime_error("cannot open code");
  std::string raw((std::istreambuf_iterator<char>(in)),{});
  unsigned char digest[SHA256_DIGEST_LENGTH];
  SHA256(reinterpret_cast<const unsigned char*>(raw.data()),raw.size(),digest);
  std::ostringstream hash;
  for(auto b:digest) hash<<std::hex<<std::setw(2)<<std::setfill('0')<<int(b);
  std::set<uint32_t> unique;size_t parsed=0,invalid=0,pos=0;
  while(pos<raw.size()) {
   size_t end=raw.find('\n',pos);if(end==std::string::npos) end=raw.size();
   std::string line=raw.substr(pos,end-pos);pos=end+1;
   bool ok=line.size()==size_t(n);
   for(unsigned char c:line) if(c<'0'||c>='0'+q) ok=false;
   if(!ok) {++invalid;continue;}
   uint64_t id=0;for(unsigned char c:line) id=id*q+(c-'0');
   ++parsed;unique.insert(uint32_t(id));
  }
  if(raw.empty()) invalid=1;
  bool canonical=!raw.empty()&&raw.back()=='\n'&&invalid==0;
  std::vector<uint8_t> dist;std::vector<uint32_t> queue;
  uint64_t covered=0,first=N;int maximum=-1;bool exhaustive=invalid==0;
  if(exhaustive) {
   dist.assign(N,255);queue.reserve(N);
   for(auto id:unique) {dist[id]=0;queue.push_back(id);}
   for(size_t head=0;head<queue.size();++head) {
    uint32_t id=queue[head];
    for(int i=0;i<n;++i) {
     int old=(id/power[i])%q;
     for(int digit=0;digit<q;++digit) {
      if(digit==old) continue;
      int64_t neighbour=int64_t(id)+(int64_t(digit)-old)*int64_t(power[i]);
      if(neighbour<0||uint64_t(neighbour)>=N) throw std::runtime_error("packing invariant");
      if(dist[neighbour]==255) {
       dist[neighbour]=dist[id]+1;queue.push_back(uint32_t(neighbour));
      }
     }
    }
   }
   for(uint64_t id=0;id<N;++id) {
    if(dist[id]!=255) maximum=std::max(maximum,int(dist[id]));
    if(dist[id]<=R) ++covered;else if(first==N) first=id;
   }
   if(!unique.empty()&&queue.size()!=N) throw std::runtime_error("missed vertices");
  }
  std::cout<<"{\"q\":"<<q<<",\"n\":"<<n<<",\"R\":"<<R
   <<",\"M_parsed\":"<<parsed<<",\"M_unique\":"<<unique.size()
   <<",\"duplicates\":"<<parsed-unique.size()<<",\"invalid_lines\":"<<invalid
   <<",\"ambient_words\":"<<N<<",\"sha256\":\""<<hash.str()<<"\""
   <<",\"canonical\":"<<(canonical?"true":"false")
   <<",\"exhaustive\":"<<(exhaustive?"true":"false")<<",\"covered\":";
  if(exhaustive) std::cout<<covered;else std::cout<<"null";
  std::cout<<",\"uncovered\":";if(exhaustive) std::cout<<N-covered;else std::cout<<"null";
  std::cout<<",\"max_min_distance\":";if(maximum>=0) std::cout<<maximum;else std::cout<<"null";
  std::cout<<",\"first_uncovered\":";
  if(!exhaustive||first==N) std::cout<<"null";
  else {std::cout<<'"';for(auto p:power) std::cout<<(first/p)%q;std::cout<<'"';}
  double sec=std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count();
  bool pass=canonical&&exhaustive&&covered==N;
  std::cout<<",\"runtime_seconds\":"<<sec<<",\"status\":\""<<(pass?"PASS":"FAIL")<<"\"}\n";
  return pass?0:1;
 } catch(const std::exception& e) {std::cerr<<e.what()<<'\n';return 2;}
}
