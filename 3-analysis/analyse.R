dataset="../tweets.gz"
df=read.csv(gzfile(dataset),header=T,quote="",sep="\t")
variables=c("yat","da_je_li","sta_sto","bre","mnogo","drug","rdrop","c_ch","months")
#for (v in variables){ print(v);print(summary(df$v))}
print(summary(df))
tusers=table(df$user)
print("Number of users: ")
print(length(tusers))
print(length(tusers[tusers>=100]))
