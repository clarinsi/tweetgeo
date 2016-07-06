# install.packages("sp")
# install.packages("leaflet")

library(sp)
library(leaflet)

#function to map and summarizes individual linguistic attributes. Input parameter: column number (attrNr)

mapTweets<-function(attrNr){
  tw.new<-tw.s[,c(lonidx,latidx,attrNr,textidx)]
  names(tw.new)<-c("y","x","attr","text")

  tw.new<-tw.new[!is.na(tw.new$attr),]
  tw.new<-tw.new[!is.na(tw.new$text),]
  
  coordinates(tw.new)<-~x+y
  proj4string(tw.new)<-CRS("+init=epsg:4326")
  
  pal <- colorFactor('RdYlBu', tw.new@data$attr)
  
  print(table(tw.new$attr))
  print(paste("n measures:",length(tw.new)))
  
  m <- leaflet(tw.new) %>%
    ##background map
    addTiles() %>%
    ##own idw raster
    addCircleMarkers(tw.new@coords[,1],tw.new@coords[,2], color=~pal(attr),radius=5,stroke=FALSE,popup = tw.new@data$text,fillOpacity = 0.5)%>%
    
    addLegend(position = 'topright',colors = ~pal(levels(attr)), labels = ~levels(attr))   
  #execute the leaflet object and thus create the visualisation
  m
}

features<-data.frame(names=names(tw.s)[7:15], attrNr=7:15)
features

#execute the function, here using the linguit. info in column 9
mapTweets(6)




