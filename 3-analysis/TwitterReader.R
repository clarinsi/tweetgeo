#reading the data
tw<-read.csv("../2-extraction/IberiaDSL.tsv",sep="\t",quote="\"",header=F)

#define lon column
lonidx<-3

#define lat column
latidx<-4

#define text column
textidx<-5
  
#define specific columns containing the linguistic variables using c(1,2,5,6,...) or create a vector of consecutive columns using 1:10
cols<-6:7

#df with only the linguistic info
tw.attr<-tw[,cols]

#calculating the number of NAs per line
tw.attr.na<-apply(tw.attr, MARGIN = 1, FUN = function(x) length(x[is.na(x)]) )

#tweets with no linguistic information are filtered
tw.s<-tw[tw.attr.na<length(cols),]


#defining the geographic extent using the latitude and longitude maximas and minimas
#minLat<-38.979303
#minLat<-38
#minLong<-11.251361
#minLong<-11
#maxLat<-47.32256
#maxLat<-48
#maxLong<-24.645286
#maxLong<-25
#tw.s<-tw.s[tw.s$lat<maxLat & tw.s$lat>minLat & tw.s$lon<maxLong & tw.s$lon>minLong,]
