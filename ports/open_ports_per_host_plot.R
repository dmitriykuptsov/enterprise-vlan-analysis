args<-commandArgs(trailingOnly=T);
dataFile<-args[1];
print(dataFile);
data<-read.csv(dataFile, sep=" ", header=F);
names(data)<-c("Port", "Protocol", "IP", "Subnetwork");
tcpData<-data[data$Protocol=="tcp", ];
agr.tcp.count <- aggregate(x=tcpData$Port, by = list(tcpData$IP), FUN=length);

# We do not have UDP ports open
#values <- data.frame(value=udpData$Port);
#agr.udp.count <- aggregate(x=values, by = list(unique.values = values$value), FUN=length);

pdf("distribution_of_ports_per_host.pdf")
hist(agr.tcp.count$x, col="dark blue", xlab="Open ports per host", ylab="Frequency", main="", xaxs="i", yaxs="i", bty="c");
grid(col="black")
box();
dev.off();

#print(agr.tcp.count);
#pdf("aggregated_ports_tcp.pdf")
#barplot(agr.tcp.count$value, names.arg=agr.tcp.count$unique.values, 
#	col="dark red", las=2, cex.axis=0.7, cex.lab=0.9, cex=0.7, horiz=T,
#	ylab="Ports", xlab="Frequency", xaxs="i", yaxs="i", bty="c", axis.lty=1);
#grid(col="black", lwd=2);
#box();
#dev.off();

#sub    <- subset(agr.tcp.count, agr.tcp.count$value > 0)
#radius <- sqrt( grid$count / pi )
#symbols(grid$Var1, grid$Var2, radius, inches=0.30, xlab="Research type", ylab="Research area")
#text(grid$Var1, grid$Var2, grid$count, cex=0.5)