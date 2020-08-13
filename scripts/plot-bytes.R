args<-commandArgs(trailingOnly=T);

tcpDataFile<-args[1];
udpDataFile<-args[2];

tcpData<-as.numeric(scan(tcpDataFile)) / 1024 / 1024;
udpData<-as.numeric(scan(udpDataFile)) / 1024 / 1024;

#p<-seq(from=0, to=1, by=0.1);
#q1<-quantile(tcpData, probs=p);
#q2<-quantile(udpData, probs=p);

pdf("distribution_of_bytes_transmitted.pdf");

par(mfrow=c(2, 1));
hist(as.numeric(tcpData), breaks=1000, col="dark blue", xlab="Megabytes transmitted by TCP applications", ylab="Frequency", main="", xaxs="i", yaxs="i", bty="c");
grid(col="black");
box();

hist(as.numeric(udpData), breaks=1000, col="dark red", xlab="Megabytes transmitted by UDP applications", ylab="Frequency", main="", xaxs="i", yaxs="i", bty="c");
grid(col="black");
box();

#plot(q1, p, col="dark blue", lwd=3, main="", xlab="Megabytes transmitted", ylab="Probability", type="l");
#points(q2, p, col="dark red", lwd=3);
#grid(col="black");

dev.off();
