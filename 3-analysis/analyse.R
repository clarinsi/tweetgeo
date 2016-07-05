dataset="../../hbs-twitter-space/hrsrTweets.var.gz"
df=read.csv(gzfile(dataset),header=T,quote="",sep="\t")
print(summary(df))
