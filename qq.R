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
  data <- data.frame(observed = corvec^2, correlation = corvec)
  data <- data[with(data, order(observed)), ]
  data$expected <- sort(nullcorvec^2)
  return(data)
}

tissue_qqR2 <- function(corvec, nn, tissue)
{
  data <- qqR2(corvec, nn)
  data$tissue <- tissue
  return(data)
}

plot_qqR2_csvs <- function(files, output_prefix)
{
    for (file_item in files) {
        file_name <- as.character(file_item)
        qqR2data <- read.table(file_name, sep='\t')
        meanr2vec <- round(mean(qqR2data$R2,na.rm=TRUE),4)
        tissue <- qqR2data$tissue[1]
        output_file_name <- paste(output_prefix, "/", tissue, ".png", sep="", collapse="")
        print(paste("plotting",output_file_name,sep=" "))
        plot_qqR2(qqR2data, meanr2vec, tissue, output_file_name)
    }
}

plot_qqR2 <- function(qqR2data, meanr2vec, tissue, output_file_name)
{
    plot<-ggplot(qqR2data,aes(x=expected,y=observed))+
            geom_point(pch=1,cex=1.5)

    p2<- plot +
        geom_abline(intercept=0, slope=1) +
         xlab(expression("Expected R"^2)) +
         ylab(expression("Observed Predictive R"^2))+
          theme_bw(20)

    ann_text <- data.frame(observed=0.8,expected=0,r2=meanr2vec,tissue=tissue)
    p3<-p2+
        geom_text(data=ann_text,aes(label=paste("mean_R^2 ==",r2,sep="")),parse=T,hjust=0,size=5)

    png(file=output_file_name,height=320,width=480)
    print(p3)
    dev.off()
}

merge_qqR2_csvs <- function(files, output_file_name)
{
    merged <- data.frame()
    meanr2vec <- vector()
    tisvec <- vector()
    for(file_item in files) {
        file_name <- as.character(file_item)
        qqR2Data <- read.table(file_name, sep='\t')

        finalres<-read.table(resfile,header=T)
        meanr2vec <- c(meanr2vec,round(mean(qqR2data$R2,na.rm=TRUE),4))

        tis<-as.character(qqR2data$tissue[1])
        tisvec<-c(tisvec,tis)
        points<-qqR2(sqrt(finalres[,1]),n,tis)
        merged<-rbind(merged,points)
    }
    return(merged)
}

plot_merged_qqR2 <- function(qqR2data, meanr2vec, tissue, output_file_name)
{
    plot<-ggplot(finalp,
        aes(x=expected,y=observed))+geom_point(pch=1,cex=1.5)+
        facet_wrap(~tissue,scales="fixed",ncol=3)

    p2<- plot +
        geom_abline(intercept=0, slope=1) +
        xlab(expression("Expected R"^2)) +
        ylab(expression("Observed Predictive R"^2)) + theme_bw(20)

    ann_text <- data.frame(obs=0.8,exp=0,r2=meanr2vec,tissue=factor(tisvec))
    p3<-p2+
        geom_text(data=ann_text,aes(label=paste("mean_R^2 ==",r2,sep="")),parse=T,hjust=0,size=5)

    png(file=output_file_name,height=720,width=720)
    print(p3)
    dev.off()
}

