
library(GISTools)

tw.spat<-tw.s
coordinates(tw.spat)<-c(latidx,lonidx)
proj4string(tw.spat)<-CRS("+init=epsg:4326")
#spplot(tw.spat[,"V1"])
  
tw.dens<-kde.points(tw.spat,h=2,n=100,lims=NULL)
tw.dens@data$kde<-(tw.dens@data$kde-min(tw.dens@data$kde))/(max(tw.dens@data$kde)-min(tw.dens@data$kde))
spplot(tw.dens)

densityTweets<-function(attrNr,filtQuart=1){
  tw.new<-tw.s[,c(lonidx,latidx,attrNr)]
  names(tw.new)<-c("y","x","attr")
  
  tw.new<-tw.new[!is.na(tw.new$attr),]

  print(table(tw.new$attr))
  
  coordinates(tw.new)<-~x+y
  proj4string(tw.new)<-CRS("+init=epsg:4326")
  
  tw.dens.feature<-tw.dens
  
  for(i in levels(tw.new@data$attr)){
    tw.sub<-subset(tw.new,attr==i)
    tw.sub.dens<-kde.points(tw.sub,h=2,n=100,lims=tw.dens.feature)
    #tw.sub.dens@data$kde<-(tw.sub.dens@data$kde-min(tw.sub.dens@data$kde))/(max(tw.sub.dens@data$kde)-min(tw.sub.dens@data$kde))
    #tw.sub.dens@data$kde<-tw.sub.dens@data$kde-tw.dens@data$kde
    
    tw.dens.feature@data[,i]<-tw.sub.dens@data$kde
  }
  
  tw.dens.feature@data$kde<-NULL
  maxLevel<-colnames(tw.dens.feature@data)[apply(tw.dens.feature@data,1,which.max)]
  maxValue<-apply(tw.dens.feature@data,1,max)
  
  values<-maxValue<sort(maxValue)[round(filtQuart*length(maxValue)/4)]
  
  maxLevel[values]<-NA
  
  tw.dens.feature.summary<-tw.dens
  tw.dens.feature.summary@data$kde<-NULL
  
  tw.dens.feature.summary@data$maxLevel<-factor(maxLevel)
  tw.dens.feature.summary@data$maxValue<-maxValue
  
  p1 = spplot(tw.dens.feature.summary, "maxLevel",col="transparent")
  p2 = spplot(tw.dens.feature.summary, "maxValue",col="transparent")
  #p0=plot(TMWorldBorders[TMWorldBorders$ISO2 %in% c("SI","HR","RS","BA","ME"),])
  #print(p0, position = c(0,0,.5,1))
  print(p1, position = c(0,0,.5,1),more=T)
  print(p2, position = c(.5,0,1,1)) 
}

features<-data.frame(names=names(tw.s)[7:15], attrNr=7:15)
features

densityTweets(6,1)
