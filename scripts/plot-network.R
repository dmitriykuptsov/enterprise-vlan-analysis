args<-commandArgs(trailingOnly=T);
library(igraph) # This loads the igraph package

#dat=read.csv(args[1],header=F,check.names=FALSE) # choose an adjacency matrix from a .csv file
dat=read.csv(args[1],header=F,sep=",") # choose an adjacency matrix from a .csv file
n=scan(args[2], what="character");
#dim(n)
m=as.matrix(dat) # coerces the data set as a matrix
g=graph.adjacency(m,mode="undirected",weighted=NULL)
#V(g)$name
V(g)$label.cex=0.6
pdf("interaction_between_local_computers_over_tcp.pdf");
plot(g, layout=layout_randomly, vertex.size=8, edge.color=c("dark red"), edge.curved=.3, vertex.color="gray40", vertex.label=as.list(n));
dev.off();
