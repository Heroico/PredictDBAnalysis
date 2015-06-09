library(ggplot2)
library(dplyr)
library(tidyr)
library(reshape2)
source("utilities.R")

qqR2 <- function(corvec,nn)
{
  set.seed( as.integer((as.double(Sys.time())*1000+Sys.getpid()) %% 2^31) )
## nn is the sample size, number of individuals used to compute correlation.
## needs correlation vector as input.
## nullcorvec generates a random sample from correlation distributions, under the null hypothesis of 0 correlation using Fisher's approximation.
  mm <- length(corvec)
  nullcorvec = tanh(rnorm(mm)/sqrt(nn-3)) ## null correlation vector
  data <- data.frame(cbind(sort(corvec^2),sort(nullcorvec^2)))
  colnames(data)<-c("observed","expected")
  return(data)
}

tissue_qqR2 <- function(corvec, nn, tissue)
{
  data <- qqR2(corvec, nn)
  data <- data %>% mutate(tissue=tissue)
  colnames(data)<-c("observed","expected","tissue")
  return(data)
}

#merge_csv_qqR2 <- function(files)
#{
#    merged <-data.frame()
#    for (file in files) {
#        file1 = paste(file,"-predicted.csv",sep="",collapse="")
#        file2 = paste(file,"-observed.csv",sep="",collapse="")
#
#        correlation_data <- correlate_csv_files(file1, file2)
#        data <- tissue_qqR2(correlation_data$Correlation, tail(correlation_data$Rows,1),file)
#        merged <- rbind(merged,data)
#    }
#    return(merged)
#}

plot_qqR2 <-function(tissue_qqR2_data)
{
    plot<-ggplot(finalp,aes(x=exp,y=obs))+
            geom_point(pch=1,cex=1.5)+
            facet_wrap(~tissue,scales="fixed",ncol=3)

    p2<- plot +
        geom_abline(intercept=0, slope=1) +
         xlab(expression("Expected R"^2)) +
         ylab(expression("Observed Predictive R"^2))+
          theme_bw(20)

    ann_text <- data.frame(obs=0.8,exp=0,r2=meanr2vec,tissue=factor(tisvec))
    p3<-p2+
        geom_text(data=ann_text,aes(label=paste("mean_R^2 ==",r2,sep="")),parse=T,hjust=0,size=5)


    png(file="FigS3_DGN-EN_to_GTEx-pilot.png",height=720,width=720)
    p3
    dev.off()
}
