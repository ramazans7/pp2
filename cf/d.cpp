#include<iostream>
#include<cctype>
#include<algorithm>
typedef long long ll;
using namespace std;
 
int main() {
  ll a;
  ll b[1000000];
  cin>>a;
  for(int i=0; i<a-1; i++){
    cin>>b[i];
  }
  sort(b, b + a - 1);
  for(int i=0; i<a-1; i++){
    if(a==2){
        if(b[i]==2){
            cout<<1;
        }
        else cout<<2;
        break;
  }
    if(b[i]+1==b[i+1]){
        continue;
    }
    else cout<<b[i]+1;
    break;
  }
}