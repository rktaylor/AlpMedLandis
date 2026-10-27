library(raster) 

converter <- function(medland_template, landis_input,landis_output, medland_output, cfactor_out_name){
  
  template <- raster(medland_template) # (contains correct UTM Zone 10 projection) 
  landis_original <- raster(landis_input) # (generic grid, no projection) 
  landis_flipped <- flip(landis_original, direction = "y") # the map is imported upside down
  
  if (ncol(template) == ncol(landis_original) && nrow(template) == nrow(landis_original)) {
    #Copy values from output to template, keeping the UTM georeferencing
    values(template) <- values(landis_flipped)
    rmin <- minValue(template)
    rmax <- maxValue(template)
    template_scaled <- (template - rmin) / (rmax - rmin) * 50
    cfactor_output <- template_scaled
    
    #Create a C factor map for use in lansdscape.evol
    
    # Extract raster values
    v <- values(cfactor_output)
    
    # 0 - 2 : 0.100 -> 0.080
    i <- v >= 0 & v <= 2
    v[i] <- 0.100 + (v[i] - 0) * (0.080 - 0.100) / (2 - 0)
    
    # 3 - 7 : 0.080 -> 0.050
    i <- v >= 3 & v <= 7
    v[i] <- 0.080 + (v[i] - 3) * (0.050 - 0.080) / (7 - 3)
    
    # 8 - 12 : 0.050 -> 0.030
    i <- v >= 8 & v <= 12
    v[i] <- 0.050 + (v[i] - 8) * (0.030 - 0.050) / (12 - 8)
    
    # 13 - 18 : 0.030 -> 0.010
    i <- v >= 13 & v <= 18
    v[i] <- 0.030 + (v[i] - 13) * (0.010 - 0.030) / (18 - 13)
    
    # 19 - 37 : 0.010 -> 0.008
    i <- v >= 19 & v <= 37
    v[i] <- 0.010 + (v[i] - 19) * (0.008 - 0.010) / (37 - 19)
    
    # 38 - 50 : 0.008 -> 0.005
    i <- v >= 38 & v <= 50
    v[i] <- 0.008 + (v[i] - 38) * (0.005 - 0.008) / (50 - 38)
    
    # Assign the modified values back to the raster
    values(cfactor_output) <- v
    
    # Save the modified maps
    writeRaster(template, landis_output, format="GTiff", overwrite=TRUE)
    writeRaster(template_scaled, medland_output, format="GTiff", overwrite=TRUE)
    writeRaster(cfactor_output, cfactor_out_name, format="GTiff", overwrite=TRUE)
  } else {
    stop("Error: Output dimensions do not match input template.")
  }
  
}

#### USE BELOW TO TEST AND RUN MANUALLY #####
template <- "ecoregions_fake_UTM_100.tif"
landis_in <- "biomass-TotalBiomass-10.tif"
landis_out <-"biomass_TotalBiomass_10_georef.tif"
medland_out <- "biomass_TotalBiomass-10_scaled.tif"
cfactor_out <- "biomass_TotalBiomass-10_cfactor.tif"
converter(template, landis_in, landis_out, medland_out, cfactor_out)

#### Added for running outside of R - Chatgpt #####
if (!interactive()) {
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) != 4) {
    stop("Usage: Rscript converter.R template.tif landis_input.tif landis_output.tif medland_output.tif")
  }
  
  converter(args[1], args[2], args[3], args[4], args[5])
}

#### Syntax for running outside of R - Chatgpt #####
# Should be Called with something like this: 
#   
# medlandis_raster_converter converter.R \
# ecoregions_fake_UTM_100.tif \
# biomass-TotalBiomass-10.tif \
# landis_output.tif \
# medland_output.tif


# 0.000:2.000:0.100:0.080
# 3.000:7.000:0.080:0.050
# 8.000:12.000:0.050:0.030
# 13.000:18.000:0.030:0.010
# 19.000:37.000:0.010:0.008
# 38.000:50.000:0.008:0.005



