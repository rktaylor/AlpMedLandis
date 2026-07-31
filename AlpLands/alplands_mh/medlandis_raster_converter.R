library(raster) 


converter <- function(medland_template, landis_input,landis_output, medland_output){
  
  template <- raster(medland_template) # (contains correct UTM Zone 10 projection) 
  landis_original <- raster(landis_input) # (generic grid, no projection) 
  landis_flipped <- flip(landis_original, direction = "y") # the map is imported upside down
  
  if (ncol(template) == ncol(landis_original) && nrow(template) == nrow(landis_original)) {
    #Copy values from output to template, keeping the UTM georeferencing
    values(template) <- values(landis_flipped)
    rmin <- minValue(template)
    rmax <- maxValue(template)
    template_scaled <- (template - rmin) / (rmax - rmin) * 50
    
    # Save the modified maps
    writeRaster(template, landis_output, format="GTiff", overwrite=TRUE)
    writeRaster(template_scaled, medland_output, format="GTiff", overwrite=TRUE)
  } else {
    # TODO - Roy - Have this routine return metadata/success or failure
    stop("Error: Output dimensions do not match input template.")
  }
  
}

#### USE BELOW TO TEST AND RUN MANUALLY #####
# template <- "ecoregions_fake_UTM_100.tif"
# landis_in <- "biomass-TotalBiomass-10.tif"
# landis_out <-"biomass_TotalBiomass_10_georef.tif"
# medland_out <- "biomass_TotalBiomass-10_scaled.tif"
# converter(template, landis_in, landis_out, medland_out)

#### Added for running outside of R - Chatgpt #####
if (!interactive()) {
  args <- commandArgs(trailingOnly = TRUE)
  
  if (length(args) != 4) {
    stop("Usage: Rscript converter.R template.tif landis_input.tif landis_output.tif medland_output.tif")
  }
  
  converter(args[1], args[2], args[3], args[4])
}

#### Syntax for running outside of R - Chatgpt #####
# Should be Called with something like this: 
#   
# medlandis_raster_converter converter.R \
# ecoregions_fake_UTM_100.tif \
# biomass-TotalBiomass-10.tif \
# landis_output.tif \
# medland_output.tif
