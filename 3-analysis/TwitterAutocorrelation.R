# install.packages("sp")
# install.packages("spatstat")

library(spatstat)
library(spdep)
library(sp)
#library(FNN)

autocorrTweets<-function(attrNr){
  tw.new<-tw.s[,c(4,5,attrNr)]
  names(tw.new)<-c("y","x","attr")
  
  tw.new<-tw.new[!is.na(tw.new$attr),]

  #if there are more than 5000 samples, a random subset of 5000 samples is selected
  if(nrow(tw.new)>5000){
    tw.new<-tw.new[round(runif(5000,1,nrow(tw.new))),]
  }

  tw.new$attr<-factor(tw.new$attr)
  if(length(levels(tw.new$attr))<2){
    return(data.frame(feature=NA, level=NA, autoCorr=NA, nValues=NA))
  }
  
  coordinates(tw.new)<-~x+y
  proj4string(tw.new)<-CRS("+init=epsg:4326")
  
  #compute nearest neighbors
  tw.knn <- knearneigh(tw.new, k=5)
  tw.nb<- knn2nb(tw.knn)
  
  #computing inverse distance weights for neighbors
  tw.nbDist <- nbdists(tw.nb, tw.new, longlat = TRUE)
  tw.nbDistI <- lapply(tw.nbDist, function(x) 1/x)
 
  #create a list of neighbors and inverse distance weights
  tw.listw <- nb2listw(tw.nb, glist=tw.nbDistI, style = "U")
  
  #calculate spatial autocorrelation -> Ho: random distribution of values (p-val > 0.05; Ho supported)
  tw.spac<-joincount.mc(tw.new@data$attr, tw.listw, 100)

  #writing output list with autcorr stat for all attributes. Each value of each variable is associated with variable name, value name and the p-val
  output<-data.frame(feature=NA, level=NA, autoCorr=NA, nValues=NA)
  for(j in 1:length(tw.spac)){
    autoCorr<-tw.spac[[j]]$p.value
    level<-gsub("Join-count statistic for ", "", names(tw.spac[[j]]$statistic))
    nValues<-nrow(subset(tw.new,attr==level))
    
    output<-rbind(output,data.frame(feature=attrNr, level=level, autoCorr=autoCorr, nValues=nValues))
  }
  output<-output[-1,]
  return(output)
}


distTweets<-function(attrNr){
  tw.new<-tw.s[,c(lon,lat,attrNr)]
  names(tw.new)<-c("y","x","attr")
  
  tw.new<-tw.new[!is.na(tw.new$attr),]

  #if there are more than 5000 samples, a random subset of 5000 samples is selected
  if(nrow(tw.new)>5000){
    tw.new<-tw.new[round(runif(5000,1,nrow(tw.new))),]
  }
  
  tw.new$attr<-factor(tw.new$attr)
  if(length(levels(tw.new$attr))<2){
    return(data.frame(feature=NA, level=NA, distLevel=NA,distFeature=NA,distRel=NA, nValues=NA))
  }
  
  coordinates(tw.new)<-~x+y
  proj4string(tw.new)<-CRS("+init=epsg:4326")
  
  tw.dist<-median(spDists(tw.new, longlat = TRUE))*1000
  
  output<-data.frame(feature=NA, level=NA, distLevel=NA,distFeature=NA,distRel=NA, nValues=NA)
  for(i in levels(tw.new@data$attr)){
    tw.sub<-subset(tw.new,attr==i)
    tw.sub.dist<-median(spDists(tw.sub, longlat = TRUE))*1000
    output<-rbind(output,data.frame(feature=attrNr,level=i,distLevel=tw.sub.dist,distFeature=tw.dist,distRel=tw.sub.dist/tw.dist,nValues=length(tw.sub)))
  }
  
  output<-output[-1,]
  return(output)
}



features<-data.frame(names=names(tw.s)[7:15], attrNr=7:15)
features

#autocorrTweets(7)

distTweets(6)



#performing the test for all features in the dataframe
autoCor.all<-data.frame(feature=NA, level=NA, autoCorr=NA, nValues=NA)
cols<-7:15
for(i in cols){
  print(i)
  output<-autocorrTweets(i)
  autoCor.all<-rbind(autoCor.all,output)
}
autoCor.all<-autoCor.all[!is.na(autoCor.all$feature),]

#performing the test for all features in the dataframe
relDist.all<-data.frame(feature=NA, level=NA, distLevel=NA,distFeature=NA,distRel=NA, nValues=NA)
cols<-7:14
for(i in cols){
  print(i)
  output<-distTweets(i)
  relDist.all<-rbind(relDist.all,output)
}
relDist.all<-relDist.all[!is.na(relDist.all$feature),]
