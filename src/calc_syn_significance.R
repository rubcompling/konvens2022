# author: Stefanie Dipper
# first: remove all variables etc. from working memory
rm(list=ls(all=TRUE))

pdf(file="results/3_syntax/significance/RPlots.pdf")
sink("results/3_syntax/significance/trends.txt")


mydata <- read.csv("results/3_syntax/significance/syntax_all.csv", 
                   sep="\t", header=TRUE)
head(mydata)
str(mydata)
summary(mydata)

################################################
# Data for each measure separately
# Mean scores

meansOverall <- with(mydata, tapply(score, list(measure), mean))
meansOverall
meansPerYear <- with(mydata, tapply(score, list(measure,year), mean))
meansPerYear

sdOverall <- with(mydata, tapply(score, list(measure), sd))
sdOverall
sdPerYear <- with(mydata, tapply(score, list(measure,year), sd))
sdPerYear

# plot all averaged scores per year
matplot(t(meansPerYear), type="l")
matplot(t(sdPerYear), type="l")

################################################
# Plots

# find trend line with regression analysis
# NOTE: it's almost 5year-steps, except once: +6 + 4 -> treat as +5!
# (1968 - 1974 - 1978)

# trend line: predict scores from years 
# -> BUT: give wrong impression that data start in year 0
# however, it does not make a difference for the slope!
# (just for the intercept)

for (mylevel in levels(mydata$measure)) {
  data.sel <- mydata[mydata$measure==mylevel, ]
  with(data.sel,
       plot(x=year, y=score, xlab="Year", ylab=mylevel))
  data.lm <- with(data.sel, lm(score ~ year))
  print(mylevel)
  print(summary(data.lm))
  abline(data.lm)
}
