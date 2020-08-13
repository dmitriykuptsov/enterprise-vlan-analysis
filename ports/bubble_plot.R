args<-commandArgs(trailingOnly=T);
dataFile<-args[1];
print(dataFile);
data<-read.csv(dataFile, sep=" ", header=F);
names(data)<-c("Port", "Protocol", "IP", "Subnetwork");
tcpData<-data[data$Protocol=="tcp", ];

values <- data.frame(port=as.factor(tcpData$Port), subnet=as.factor(tcpData$Subnetwork));

agr.tcp.count <- aggregate(cbind(port, subnet)~port+subnet, values, FUN=length);
agr.tcp.count <- data.frame(port=agr.tcp.count[, 1], subnet=agr.tcp.count[, 2], count=agr.tcp.count[, 3]);


# Compute the levels for ports and subnetwork fields
# Use these values as marks on the axis

x_at <- seq_along(levels(agr.tcp.count$subnet))
x_labels <-   levels(agr.tcp.count$subnet)
y_at <- seq_along(levels(agr.tcp.count$port))
y_labels <-   levels(agr.tcp.count$port)

pdf("bubble_plot_distribution_of_open_ports.pdf")
radius <- sqrt( agr.tcp.count$count / pi )
symbols(agr.tcp.count$subnet, agr.tcp.count$port, circles=radius, 
	inches=0.30, ylab="Port number", xlab="", 
	las=2, xaxs="i", yaxs="i", xaxt = "n", yaxt = "n",
	cex.axis=0.7, cex.lab=0.9, cex=0.7, bg=rgb(0.8, 0.5, 0.5, 0.5))

print(sqrt(max(agr.tcp.count$count)/pi));
print(sqrt(min(agr.tcp.count$count)/pi));
print(sqrt(mean(agr.tcp.count$count)/pi));

symbols(1, 0, circles=sqrt(max(agr.tcp.count$count)/pi), inches=0.30, add=T, bg=rgb(0.5, 0.5, 0.5, 0.5));
text(1, 0, "# of hosts", cex=0.5);

#symbols(1 + sqrt(max(agr.tcp.count$count)/pi) - sqrt(mean(agr.tcp.count$count)/pi), 0, circles=sqrt(mean(agr.tcp.count$count)/pi), inches=0.30, add=T);
#symbols(1 + sqrt(max(agr.tcp.count$count)/pi) - sqrt(min(agr.tcp.count$count)/pi), 0, circles=sqrt(min(agr.tcp.count$count)/pi), inches=0.30, add=T);

#symbols(1.5, 0, circles=sqrt(mean(agr.tcp.count$count)/pi), 
#	inches=0.30, add=T, bg=rgb(0.5, 0.5, 0.5, 0.5));

#symbols(2, 0, circles=sqrt(min(agr.tcp.count$count)/pi), 
#	inches=0.30, add=T, bg=rgb(0.5, 0.5, 0.5, 0.5));

grid(col="black", ny=length(y_at), nx=length(x_at));
axis(side=1, at=x_at, labels=x_labels, las=2, cex.axis=0.7, cex.lab=0.9, cex=0.7)
axis(side=2, at=y_at, labels=y_labels, las=2, cex.axis=0.7, cex.lab=0.9, cex=0.7)

dev.off();