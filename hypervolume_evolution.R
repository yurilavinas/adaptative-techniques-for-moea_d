rm(list = ls(all = TRUE))
setwd("~/MOEADr/R/")
library(MOEADr)
library(emoa)
library(ggplot2)

# names of algorithms in analysis
names <- c(
  "no_adaptation",
  "adaptation"
)

checkpoints <- (0:300) * 500

seed = 742
repetitions = 10  - 1
ref.point <- c(1.1, 1.1, 1.1)
fun = "uf9"
n_obj = 3

#function for loading pareto fronts data
loadPlotData <- function (iter, wd = '~/dataExp/') {
  Y <-
    read.csv(paste0(wd, iter, '_paretos.csv'),
             sep = " ",
             header = F)[,0:n_obj]
  temp <-
    read.csv(paste0(wd, iter, '_info_gen.csv'),
             sep = " ",
             header = F)
  
  out <- list(Y           = Y,
              nfe         = temp[1, ],
              n.iter      = temp[2, ])
  return(out)
}

getminP <- function(X){
  apply(X, MARGIN = 2, FUN = min, na.rm = TRUE)
}

getmaxP <- function(X){
  apply(X, MARGIN = 2, FUN = max, na.rm = TRUE)
}

scaling_Y <- function(Y){
  
  MinP <- matrix(rep(minP, times = nrow(Y)),
                 nrow  = nrow(Y),
                 byrow = TRUE)
  MaxP <- matrix(rep(maxP, times = nrow(Y)),
                 nrow  = nrow(Y),
                 byrow = TRUE)
  
  # Perform linear scaling
  Y    <- (Y - MinP) / (MaxP - MinP + 1e-16)
  return (Y)
}


# loading pareto fronts from all outputs of the exp for analysis - for HV scaling
ref1 <- data.frame()
for (i in seed:(seed+repetitions)) {
  for (name in names) { # loop trough algorithms in analysis
    moea = loadPlotData(i,
                      paste0("~/../../../Volumes/HD-PNFU3/temp_exp/", name, "/final/",fun, "_"))
    ref1 <-
    rbind(
      ref1,
      moea$Y
    )
  }
}

minP <- getminP(ref1)
maxP <- getmaxP(ref1)

rm(ref1)

# calculating HV 
fun_hv <- data.frame()
for (name in names) { # loop trough algorithms in analysis
  total_hv <- data.frame()
  for (i in seed:(seed+repetitions)) {
    moea <- loadPlotData(i,
                         paste0("~/../../../Volumes/HD-PNFU3/temp_exp/", name, "/final/",fun, "_"))
    n.iter <- as.integer(moea$n.iter)
    my_hv <- data.frame()
    my_sum <- 0
    ck_idx <- 1
    for (j in 1:n.iter) {
      output = loadPlotData(j, paste0("~/../../../Volumes/HD-PNFU3/temp_exp/",name,"/history/", fun, "_", i, "/"))        
      if (output$nfe >= checkpoints[ck_idx]) {
        PF <- output$Y
        nndom.idx <- find_nondominated_points(PF)
        PF <- scaling_Y(PF[nndom.idx,])
        hv <- dominated_hypervolume(t(PF), ref = ref.point)
        my_hv <-
          rbind(my_hv, cbind(hv = hv, iter = checkpoints[ck_idx]))
        ck_idx <- ck_idx + 1
      }
    }
    total_hv <- rbind(total_hv, my_hv)
  }
  
  fun_hv <-
    rbind(fun_hv, cbind(total_hv, strategy = name))
}

median <-
  aggregate(fun_hv$hv, median, by = list(fun_hv$strategy, fun_hv$iter))
sd <-
  aggregate(fun_hv$hv, sd, by = list(fun_hv$strategy, fun_hv$iter))
plot_data <- (data.frame(median, sd))
plot_data <- plot_data[,-c(4, 5)]
colnames(plot_data) <- c("PF_NUMBER", "iter", "median", "sd")
plot_data$ymax <- plot_data$median + plot_data$sd
plot_data$ymin <- plot_data$median - plot_data$sd

v <- ggplot(data = plot_data,
            aes(
              x = iter,
              y = median,
              group = PF_NUMBER,
              color = PF_NUMBER,
              fill = PF_NUMBER
            )) + 
  geom_point(aes(color = PF_NUMBER)) + theme_minimal() +
  geom_line(aes(color = PF_NUMBER)) + 
  geom_ribbon(aes(ymin =ymax, ymax = ymin),alpha = .2, linetype = 0) +
  theme(
    legend.text = element_text(size =
                                 16),
    axis.text = element_text(size =
                               24),
    axis.title =
      element_text(size = 26) 
  )  +
  labs(title = "DTLZ7", x = "Number of Function Evalutions", y = "HV", main = "DLTZ7")

print(v)
filename = paste0("~/", fun , "hv_evolution.png")
ggsave(filename = filename,
       dpi = 600,
       width = 9)


boxplot.data = fun_hv[fun_hv$iter==max(fun_hv$iter),]
u <- ggplot(data = boxplot.data,
            aes(
              x = strategy,
              y = hv,
              group = strategy,
              color = strategy,
              fill = strategy
            )) + 
  geom_boxplot(aes(color = strategy)) + theme_minimal()
print(u)
filename = paste0("~/", fun , "hv_boxplot.png")
ggsave(filename = filename,
       dpi = 600,
       width = 9)
