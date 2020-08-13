args<-commandArgs(trailingOnly=T);

data<-read.csv(args[1], header=F);

pdf("distribution_of_frame_sizes.pdf");
par(mfrow=c(2, 1));
hist(as.numeric(data$V1), breaks=30, col="dark blue", probability=T, xlab="Frame size (bytes)", ylab="Frequency", main="Distribution of frame sizes", xaxs="i", yaxs="i", bty="c");
grid(col="black");
box();
y<-seq(0, 1, 0.1);
q<-quantile(data$V1, probs=y);
plot(q, y, type="l", ylab="Probability", xlab="Frame sizes", lwd=4, col="dark red", xaxs="i", yaxs="i", bty="c");
grid(col="black");
box();

dev.off();
