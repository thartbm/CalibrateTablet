getOffset <- function() {
  
  center_data <- read.csv('tablet_calibration_data_center.csv', stringsAsFactors = FALSE)
  
  start_x <- mean(center_data$x)
  start_y <- mean(center_data$y)
  
  edge_data <- read.csv('tablet_calibration_data_circle_edge.csv', stringsAsFactors = FALSE)
  
  cf <- Reach::circleFit(X=edge_data$x, Y=edge_data$y, r = 550, fitr=TRUE)
  
  print(cf)
  
  cpar <- cf$par
  print(cpar)
  cx <- cpar[['xc']]
  cy <- cpar[['yc']]
  r <- cpar[['r']]
  
  xlims <- c(cx-r, cx+r) * 1.1
  ylims <- c(cy-r, cy+r) * 1.1
  
  print(xlims)
  print(ylims)
  
  plot(edge_data$x, edge_data$y, xlim=xlims, ylim=ylims, asp=1, col='#BBBBFF')
  
  angles <- seq(-pi, pi, length.out = 361)
  lines(cx + r * cos(angles), cy + r * sin(angles), col='red', lwd=2)
  
}