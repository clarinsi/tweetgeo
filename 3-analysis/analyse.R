#dataset="../../hbs-twitter-space/hrsrTweets.var.gz"
#variables=c("tid","user","time","lat","lon","text","yat","da_je_li","sta_sto","bre","mnogo","drug","rdrop","c_ch","months")
#df=read.csv(gzfile(dataset),header=T,quote="",sep="\t")
#df=subset(df,select=variables)
#write.table(df,file=gzfile("tweets.gz","w"),sep="\t",col.names=T,quote=F,row.names=F)
dataset="tweets.toy.gz"
df=read.csv(gzfile(dataset),header=T,quote="",sep="\t")
variables=c("yat","da_je_li","sta_sto","bre","mnogo","drug","rdrop","c_ch","months")
#for (v in variables){ print(v);print(summary(df$v))}
print(summary(df))
tusers=table(df$user)
print("Number of users: ")
print(length(tusers))
print(length(tusers[tusers>=100])
