args<-commandArgs(trailingOnly=T);

dataFile<-args[1];
data<-as.numeric(scan(dataFile));

print(data[data>1500]);

pdf("distribution_of_packet_lengths.pdf");

#par(mfrow=c(2, 1));
hist(as.numeric(data), col="dark blue", xlab="Packet length (bytes)", ylab="Probability", main="", xaxs="i", yaxs="i", bty="c", freq=F);
grid(col="black");
box();

dev.off();
