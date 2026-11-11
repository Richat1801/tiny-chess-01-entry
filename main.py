import json,os,urllib.request as U
V=[0,100,320,330,500,900,0]
DG=[-17,-15,15,17];OR=[-16,16,-1,1];KD=DG+OR
ND=[-33,-31,-18,-14,14,18,31,33];D={2:ND,6:KD,3:DG,4:OR,5:KD}
CST={1:((1,(117,118),119,118),(2,(113,114,115),112,114)),-1:((4,(5,6),7,6),(8,(1,2,3),0,2))}
RC={119:1,112:2,7:4,0:8}
B=[];KG=[0,0];NDC=[0];INF=100000;STK=[]
def parse(fen):
 global B,S,C,KG,PH
 p=fen.split();B=[0]*128;i=0;PH=0
 for ch in p[0]:
  if ch=='/':i+=8
  elif ch.isdigit():i+=int(ch)
  else:
   v='pnbrqk'.index(ch.lower())+1;B[i]=v*(1 if ch.isupper()else -1);PH+=V[v]if 2<=v<=5 else 0;i+=1
 S=1 if p[1]=='w'else -1
 C=('K'in p[2])|('Q'in p[2])<<1|('k'in p[2])<<2|('q'in p[2])<<3
 KG[0]=B.index(6);KG[1]=B.index(-6)
def atk(sq,by):
 for d in(15,17):
  t=sq+by*d
  if not t&0x88 and B[t]==by:return 1
 for j,d in enumerate(ND+KD):
  t=sq+d
  if not t&0x88 and B[t]==by*(2 if j<8 else 6):return 1
 for dirs,k0 in((DG,3),(OR,4)):
  for d in dirs:
   t=sq+d
   while not t&0x88:
    pc=B[t]
    if pc:
     if pc*by>0 and abs(pc)in(5,k0):return 1
     break
    t+=d
 return 0
def gen(caps=0):
 ms=[]
 for sq in range(128):
  if sq&0x88 or not B[sq]:continue
  pc=B[sq]
  if(pc>0)!=(S>0):continue
  k=abs(pc)
  if k==1:
   st=-16*S;one=sq+st;tg=[]
   if not B[one]:tg.append(one)
   for df in(-1,1):
    to=one+df
    if not to&0x88 and B[to]and(B[to]>0)!=(S>0):tg.append(to)
   for to in tg:
    if to>>4 in(0,7):
     for pr in(5,4,2):ms.append(sq|to<<7|pr<<14)
    elif not caps or to!=one:ms.append(sq|to<<7)
   if not caps and one in tg and sq>>4==(6 if S>0 else 1)and not B[sq+2*st]:ms.append(sq|(sq+2*st)<<7)
  else:
   for d in D[k]:
    to=sq+d
    while not to&0x88:
     vic=B[to]
     if not vic:
      if not caps:ms.append(sq|to<<7)
     else:
      if(vic>0)!=(S>0):ms.append(sq|to<<7)
      break
     if k in(2,6):break
     to+=d
   if k==6 and not caps and sq==(116 if S>0 else 4):
    for bit,emp,rq,dst in CST[S]:
     if C&bit and B[rq]==4*S and all(not B[e]for e in emp):ms.append(sq|dst<<7|1<<18)
 return ms
def make(m):
 global S,C
 STK.append((B[:],C,KG[0],KG[1]));fr,to,pr=m&127,(m>>7)&127,(m>>14)&7;pc=B[fr]
 B[to]=pr*S if pr else pc;B[fr]=0
 if abs(pc)==6:KG[pc<0]=to;C&=~3 if pc>0 else~12
 if m&1<<18:
  rf,rt=(to+1,to-1)if to&7==6 else(to-2,to+1);B[rt],B[rf]=B[rf],0
 C&=~(RC.get(fr,0)|RC.get(to,0));S=-S
def undo():
 global S,C
 o=STK.pop();B[:]=o[0];C=o[1];KG[0],KG[1]=o[2],o[3];S=-S
def ev():
 sc=0
 for sq in range(128):
  if sq&0x88 or not B[sq]:continue
  pc=B[sq];k,r=abs(pc),sq>>4;adv=7-r if pc>0 else r
  ct=(3.5-abs((sq&7)-3.5))+(3.5-abs(r-3.5));v=V[k]
  if k==1:v+=adv*10+adv*adv*2
  elif k<6:v+=int(ct*(7,4,2,3)[k-2])
  else:v+=int((7-ct)*6 if PH>1400 else ct*9)
  sc+=v if pc>0 else-v
 return sc
def srch(d,a,b,ply):
 if atk(KG[S>0],S):return INF-ply
 NDC[0]+=1
 if NDC[0]>24000:raise TimeoutError
 if d<=0:
  stand=ev()*S
  if stand>=b:return b
  a=max(a,stand);ms=gen(1)
 else:ms=gen()
 ms.sort(key=lambda m:V[abs(B[(m>>7)&127])],reverse=True)
 best=-10*INF
 for m in ms:
  if abs(B[(m>>7)&127])==6:continue
  make(m);s=-srch(d-1,-b,-a,ply+1);undo()
  if s>best:best=s
  if s>a:a=s
  if a>=b:break
 if best<=-9*INF:return-INF+ply if atk(KG[S<0],-S)else(a if d<=0 else 0)
 return a if d<=0 else best
def choose(fen):
 parse(fen);NDC[0]=0;ms=[]
 for m in gen():
  make(m)
  if not atk(KG[S>0],S):ms.append(m)
  undo()
 best=ms[0]
 for d in range(1,33):
  try:
   rm=[best]+[x for x in ms if x!=best];a=-10*INF;rb=rm[0]
   for m in rm:
    make(m);s=-srch(d-1,-10*INF,-a,1);undo()
    if s>a:a,rb=s,m
   best=rb
  except TimeoutError:break
 fr,to,pr=best&127,(best>>7)&127,(best>>14)&7
 return chr(97+(fr&7))+str(8-(fr>>4))+chr(97+(to&7))+str(8-(to>>4))+('nbrq'[pr-2]if pr else'')
def post(path,body):
 return json.load(U.urlopen(U.Request(URL+path,data=json.dumps(body).encode(),headers={'content-type':'application/json'})))
URL=os.environ['MAKEFUN_ENV_URL']
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  mv=choose(g['fen'])
  if mv not in g['legal_moves']:mv=g['legal_moves'][0]
  g=post('/move',{'game':g['game'],'move':mv})
