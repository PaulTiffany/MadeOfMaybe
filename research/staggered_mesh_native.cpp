// Independent complete native B3/S23 audit of staggered 35-turn WE.
// At g0..6000 compare whole-world evolution to evolution of each isolated
// physical component. At g6000..7600 permit intentional shared row-eater
// collisions, then assert exact world snapshots with Python.
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;
using S=unordered_set<U>;
inline U pack(int x,int y){return ((U)(uint32_t)x<<32)|uint32_t(y);}
inline int xx(U v){return (int32_t)(uint32_t)(v>>32);}
inline int yy(U v){return (int32_t)(uint32_t)v;}
S evolve(const S& world){
 unordered_map<U,uint8_t> count;
 count.reserve(world.size()*5+1);
 for(U p:world){
  int x=xx(p),y=yy(p);
  for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++){
   if(!dx&&!dy)continue;
   U q=pack(x+dx,y+dy);
   auto it=count.find(q);
   if(it==count.end())count.emplace(q,1);
   else ++it->second;
  }
 }
 S next;
 next.reserve(world.size()*2+1);
 for(auto &kv:count)
  if(kv.second==3||(kv.second==2&&world.count(kv.first)))
   next.insert(kv.first);
 return next;
}
void save(const char* path,const S& world){
 ofstream out(path);
 if(!out)throw runtime_error("cannot write snapshot");
 for(U p:world)out<<xx(p)<<' '<<yy(p)<<'\n';
}
int main(int argc,char**argv){
 if(argc<6){
  cerr<<"usage: mesh_native seed.tsv endgen final.tsv independent_until formation.tsv [frames.bin]\n";
  return 2;
 }
 try{
  int total=stoi(argv[2]),independent_until=stoi(argv[4]);
  int units;
  ifstream in(argv[1]);
  if(!(in>>units)||units<1||units>10000)throw runtime_error("bad component count");
  vector<S> parts(units);
  int id,x,y;
  while(in>>id>>x>>y){
   if(id<0||id>=units)throw runtime_error("component index out of bounds");
   parts[id].insert(pack(x,y));
  }
  S world;
  size_t total_input=0;
  for(auto &part:parts){
   total_input+=part.size();
   world.insert(part.begin(),part.end());
  }
  if(world.size()!=total_input)throw runtime_error("initial component overlap");
  cerr<<"initial "<<world.size()<<" cells in "<<units<<" physical components\n";
  ofstream frames;
  if(argc>=7)frames.open(argv[6],ios::binary);
  for(int g=0;g<=total;g++){
   if(g<=independent_until){
    S expected;
    for(auto &part:parts)expected.insert(part.begin(),part.end());
    if(expected!=world){
     cerr<<"UNLAWFUL COMPONENT INTERACTION g="<<g
         <<" whole="<<world.size()<<" independent="<<expected.size()<<"\n";
     return 3;
    }
   }
   if(g==independent_until)save(argv[5],world);
   if(frames.is_open()&&(g%32==0||g==total)){
    uint32_t count=(uint32_t)world.size();
    int32_t generation=g;
    frames.write((char*)&generation,4);
    frames.write((char*)&count,4);
    for(U p:world){
     int32_t x=xx(p),y=yy(p);
     frames.write((char*)&x,4);
     frames.write((char*)&y,4);
    }
   }
   if(g%1000==0)cerr<<"g="<<g<<" population="<<world.size()<<"\n";
   if(g<total){
    world=evolve(world);
    if(g<independent_until)for(auto& part:parts)part=evolve(part);
   }
  }
  save(argv[3],world);
  cerr<<"Native B3/S23 completed through g"<<total
      <<" final population "<<world.size()<<"\n";
  return 0;
 }catch(const exception& e){cerr<<"ERROR "<<e.what()<<"\n";return 4;}
}
