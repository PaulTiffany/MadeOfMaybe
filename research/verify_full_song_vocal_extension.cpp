// Exact 53-episode V-stem -> native lip tile in the ORIGINAL singer scene.
// Whole-song B3/S23 equivalence proof: compute dynamic V and preserved singer
// independently, check TWO-cell Moore halo separation EVERY generation.
// As local Game of Life updates have radius one, separation >=3 ensures that
// their union evolves exactly as one universe. Singer becomes fixed by g4096.
// No frame overlays, artificial cell insertions, or approximated output poses.
// Usage: /tmp/verify_v native_singer_53_vocal_components.tsv native_53_vocal_events.tsv
#include <bits/stdc++.h>
using namespace std;using U=uint64_t;using S=unordered_set<U>;
inline U pk(int x,int y){return (U(uint32_t(x))<<32)|uint32_t(y);}
inline int xx(U v){return int32_t(uint32_t(v>>32));}
inline int yy(U v){return int32_t(uint32_t(v));}
S evolve(const S&a){
 unordered_map<U,uint8_t> ns;ns.reserve(a.size()*6);
 for(U v:a){int x=xx(v),y=yy(v);
  for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++)
   if(dx||dy)ns[pk(x+dx,y+dy)]++;}
 S b;b.reserve(a.size()*2+1);
 for(auto &[v,n]:ns)if(n==3||(n==2&&a.count(v)))b.insert(v);
 return b;
}
int main(int argc,char **argv){
 if(argc!=3){cerr<<"usage: verify_v components.tsv events.tsv\n";return 2;}
 ifstream f(argv[1]);int n,i,x,y;f>>n;if(n!=6)return 3;
 vector<S> parts(n);
 while(f>>i>>x>>y){if(i<0||i>=n)return 3;parts[i].insert(pk(x,y));}
 if(vector<size_t>{parts[0].size(),parts[1].size(),parts[2].size(),
                    parts[3].size(),parts[4].size(),parts[5].size()}
      !=vector<size_t>{6408,742,0,52,1372,795})return 4;
 S base,voice=parts[5];
 for(i=0;i<5;i++)base.insert(parts[i].begin(),parts[i].end());
 if(base.size()!=8574||voice.size()!=795)return 4;
 for(U c:voice)if(base.count(c))return 5;
 ifstream e(argv[2]);struct Episode{int index,on,off;};vector<Episode> es;
 while(e>>i>>x>>y)es.push_back({i,x,y});
 if(es.size()!=53||es.front().on!=672||es.back().off!=44850)return 6;
 int formed=0,erased=0;
 const int LAST=44862,STATIC_G=4096;
 for(int g=0;g<=LAST;g++){
   // Real every-generation Life locality proof -- not a sampled heuristic.
   for(U c:voice){int cx=xx(c),cy=yy(c);
      for(int dx=-2;dx<=2;dx++)for(int dy=-2;dy<=2;dy++)
       if(base.count(pk(cx+dx,cy+dy))){
          cerr<<"ERROR actual source intersects singer halo at g="<<g<<"\n";
          return 7;
       }
   }
   for(auto a:es)if(g==a.on+2||g==a.off+4){
      bool block=voice.count(pk(991,-933))&&voice.count(pk(992,-933))&&
                 voice.count(pk(991,-932))&&voice.count(pk(992,-932));
      if(g==a.on+2){if(!block){cerr<<"missing on "<<a.index<<"\n";return 8;}formed++;}
      if(g==a.off+4){if(block){cerr<<"missing off "<<a.index<<"\n";return 9;}erased++;}
   }
   if(g==STATIC_G&&evolve(base)!=base){
      cerr<<"old singer not stable after final opening dynamics\n";return 10;
   }
   if(g<LAST){if(g<STATIC_G)base=evolve(base);voice=evolve(voice);}
 }
 if(!voice.empty()||base.size()!=7164||formed!=53||erased!=53)return 11;
 cout<<"PASS original W+V singer and WE+MADE world; 53 vocal onset/offset"
        " cycles; all 44862 Life generations exact spatial independence;"
        " 795 source cells and zero dynamic debris.\n";
 cout<<"NOT QUALIFIED: seven other physical lip targets or 403-word W."
        "\n";
 return 0;
}
