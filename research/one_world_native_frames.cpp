// Actual one-universe native B3/S23 replay. Every output frame is a complete
// whole-world state; no per-component masks, inserted glyphs or timed actor poses.
// Input: complete initial Life universe as two signed integers x y per line.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;using S=unordered_set<U>;
inline U pack(int x,int y){return (U(uint32_t(x))<<32)|uint32_t(y);}
inline int xx(U p){return int32_t(uint32_t(p>>32));}
inline int yy(U p){return int32_t(uint32_t(p));}
S evolve(const S& cells){
 unordered_map<U,unsigned char> ns;ns.reserve(cells.size()*7);
 for(U p:cells){int x=xx(p),y=yy(p);
  for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++){
   if(dx||dy){U q=pack(x+dx,y+dy);auto it=ns.find(q);
   if(it==ns.end())ns.emplace(q,1);else ++it->second;}
  }
 }
 S out;out.reserve(cells.size()*2);
 for(auto const& kv:ns){auto n=kv.second;
  if(n==3||(n==2&&cells.count(kv.first)))out.insert(kv.first);
 }
 return out;
}
int main(int argc,char**argv){
 if(argc!=5){cerr<<"usage: native input.tsv output.bin end_generation sample_step\n";return 2;}
 int end=stoi(argv[3]),step=stoi(argv[4]);
 if(end<0||step<1||end%step){cerr<<"invalid generations\n";return 2;}
 ifstream in(argv[1]);ofstream out(argv[2],ios::binary);
 if(!in||!out){cerr<<"file error\n";return 2;}
 S world;int x,y;while(in>>x>>y)world.insert(pack(x,y));
 cerr<<"g0 population "<<world.size()<<"\n";
 if(world.empty()){cerr<<"empty input initial world\n";return 3;}
 for(int g=0;g<=end;g++){
  if(g%step==0){int32_t gen=g;uint32_t count=world.size();
   out.write((char*)&gen,4);out.write((char*)&count,4);
   for(U v:world){x=xx(v);y=yy(v);
    out.write((char*)&x,4);out.write((char*)&y,4);
   }
  }
  if(g%512==0)cerr<<"g"<<g<<" population="<<world.size()<<"\n";
  if(g<end)world=evolve(world);
 }
 cerr<<"Exact full-world B3/S23 to g"<<end<<" complete\n";
 return 0;
}
