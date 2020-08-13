args<-commandArgs(trailingOnly=T);
dataFile<-args[1];
print(dataFile);
data<-read.csv(dataFile, sep=" ", header=F);
names(data)<-c("Port", "Protocol", "IP", "Subnetwork");
tcpData<-data[data$Protocol=="tcp", ];
#udpData<-data[data$Protocol=="udp", ];


values <- data.frame(value=tcpData$Port);
agr.tcp.count <- aggregate(x=values, by = list(unique.values = values$value), FUN=length);
# We do not have UDP ports open
#values <- data.frame(value=udpData$Port);
#agr.udp.count <- aggregate(x=values, by = list(unique.values = values$value), FUN=length);


#print(agr.tcp.count);
pdf("aggregated_ports_tcp.pdf")
barplot(agr.tcp.count$value, names.arg=agr.tcp.count$unique.values, 
	col="dark red", las=2, cex.axis=0.7, cex.lab=0.9, cex=0.7, horiz=T,
	ylab="Ports", xlab="Frequency", xaxs="i", yaxs="i", bty="c", axis.lty=1);
grid(col="black", lwd=2);
box();
dev.off();
