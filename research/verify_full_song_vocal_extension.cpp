// Gate 43 later isolated-Suno V episodes onto TWO EXISTING original singer lip
// locations, without touching original W->lip and original 20s three-state song.
//
// Independently evolves original native singer+WE+MADE and both real glider
// control banks. Every generation it proves that 2-cell neighborhoods of
// the banks remain disjoint; this implies their union evolves identically
// under one B3/S23 world (local radius one), not a compositor overlay.
// Verifies 86 actual block make and 86 erase checkpoints, and exact reset.
// No demand that a third, unqualified lip bank works.
//
// Usage: /tmp/test_v components.tsv episodes.tsv
#include <bits/stdc++.h>
using namespace std;
using U=uint64_t;using S=unordered_set<U>;
inline U pk(int x,int y){return (U(uint32_t(x))<<32)|uint32_t(y);}
inline int xx(U v){return int32_t(uint32_t(v>>32));}
inline int yy(U v){return int32_t(uint32_t(v));}
S evolve(const S&a){
 unordered_map<U,uint8_t> ns;ns.reserve(a.size()*7+1);
 for(U v:a){int x=xx(v),y=yy(v);
  for(int dx=-1;dx<=1;dx++)for(int dy=-1;dy<=1;dy++)
   if(dx||dy)ns[pk(x+dx,y+dy)]++;}
 S b;b.reserve(a.size()*2+1);
 for(auto &[v,n]:ns)if(n==3||(n==2&&a.count(v)))b.insert(v);
 return b;
}
bool near(const S&a,const S&b){
 if(a.empty()||b.empty())return false;
 const S& smaller=a.size()<=b.size()?a:b;
 const S& larger=a.size()<=b.size()?b:a;
 for(U v:smaller){int x=xx(v),y=yy(v);
   for(int dx=-2;dx<=2;dx++)for(int dy=-2;dy<=2;dy++)
     if(larger.count(pk(x+dx,y+dy)))return true;
 }
 return false;
}
bool hasblock(const S&s,int x,int y){
 return s.count(pk(x,y))&&s.count(pk(x+1,y))&&
        s.count(pk(x,y+1))&&s.count(pk(x+1,y+1));
}
int main(int argc,char**argv){
 if(argc!=3){cerr<<"usage: test_v components.tsv episodes.tsv\n";return 2;}
 ifstream f(argv[1]);int n,i,x,y;f>>n;if(n!=7){cerr<<"bad part count "<<n<<"\n";return 3;}
 vector<S> a(n);
 while(f>>i>>x>>y){if(i<0||i>=n)return 3;a[i].insert(pk(x,y));}
 const vector<size_t> want={6408,742,240,52,1372,645,645};
 for(i=0;i<n;i++)if(a[i].size()!=want[i]){
     cerr<<"part "<<i<<" size "<<a[i].size()<<" expected "<<want[i]<<"\n";return 4;
 }
 S singer,medium=a[5],open=a[6];
 for(i=0;i<5;i++)singer.insert(a[i].begin(),a[i].end());
 if(singer.size()!=8814||medium.size()!=645||open.size()!=645){
    cerr<<"initial group populations wrong\n";return 5;
 }
 ifstream f2(argv[2]);
 struct Event{int id,on,off;};vector<Event> events;
 while(f2>>i>>x>>y)events.push_back({i,x,y});
 if(events.size()!=43||events.front().id!=10||events.front().on!=4992||
    events.back().id!=52||events.back().off!=44850){
    cerr<<"the original Suno source was replaced\n";return 6;
 }
 int checked_make=0,checked_erase=0;
 const int last=44862, stationary_at=4096;
 for(int g=0;g<=last;g++){
   if(near(singer,medium)||near(singer,open)||near(medium,open)){
       cerr<<"UNQUALIFIED physical collision/coupling at generation "<<g
           <<" populations singer="<<singer.size()
           <<" medium="<<medium.size()<<" open="<<open.size()<<"\n";
       return 7;
   }
   for(const auto& e:events){
      if(g==e.on+2){
         if(!hasblock(medium,991,-933)||!hasblock(open,1046,-862)){
            cerr<<"Native mouth make missing for episode "<<e.id<<" g"<<g<<"\n";
            return 8;
         }checked_make++;
      }
      if(g==e.off+4){
         if(hasblock(medium,991,-933)||hasblock(open,1046,-862)){
            cerr<<"Native mouth erase missing for episode "<<e.id<<" g"<<g<<"\n";
            return 9;
         }checked_erase++;
      }
   }
   if(g==stationary_at&&evolve(singer)!=singer){
       cerr<<"Original actor not stationary after original native opening\n";
       return 10;
   }
   if(g<last){
       if(g<stationary_at)singer=evolve(singer);
       medium=evolve(medium);open=evolve(open);
   }
 }
 if(!medium.empty()||!open.empty()||singer.size()!=7164||
     checked_make!=43||checked_erase!=43){
    cerr<<"Unqualified debris or checkpoints: "<<medium.size()<<" "
        <<open.size()<<" "<<singer.size()<<" "<<checked_make<<" "<<checked_erase<<"\n";
    return 11;
 }
 cout<<"PASS 43 Suno V episodes, TWO preserved singer lip cells,"
       <<" 86 physical ON and 86 physical OFF checks at exact source times,"
       <<" 44862 actual B3/S23 source generations, full source ablation."
       <<"\n";
 cout<<"NOT YET QUALIFIED: six other lip tiles and full 403-word W-to-mouth."
       <<"\n";
 return 0;
}
