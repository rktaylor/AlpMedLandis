test -r /home/moss/.alias && source /home/moss/.alias
setopt PROMPT_SUBST
PS1='GRASS : %1~ > '
grass_prompt() {
    MAPSET_PATH="`g.gisenv get=GISDBASE,LOCATION_NAME,MAPSET separator='/'`"
    _GRASS_DB_PLACE="`g.gisenv get=LOCATION_NAME,MAPSET separator='/'`"
    
    local z_lo=`g.gisenv get=LOCATION_NAME`
    local z_ms=`g.gisenv get=MAPSET`
    ZLOC="Mapset <$z_ms> in <$z_lo>"
    if [ "$_grass_old_mapset" != "$MAPSET_PATH" ] ; then
        fc -A -I
        HISTFILE="$MAPSET_PATH/.zsh_history"
        fc -R
        _grass_old_mapset="$MAPSET_PATH"
    fi
    
    if test -f "$MAPSET_PATH/cell/MASK" && test -d "$MAPSET_PATH/grid3/RASTER3D_MASK" ; then
        echo "[2D and 3D raster MASKs present]"
    elif test -f "$MAPSET_PATH/cell/MASK" ; then
        echo "[Raster MASK present]"
    elif test -d "$MAPSET_PATH/grid3/RASTER3D_MASK" ; then
        echo "[3D raster MASK present]"
    fi
}
PROMPT_COMMAND=grass_prompt
precmd() { eval "$PROMPT_COMMAND" }
RPROMPT='${ZLOC}'
export HOME="/home/moss"
export PATH="/home/moss/miniconda3/envs/medlands/grass84/bin:/home/moss/miniconda3/envs/medlands/grass84/scripts:/home/moss/.grass8/addons/bin:/home/moss/.grass8/addons/scripts:/home/moss/miniconda3/envs/medlands/bin:/home/moss/miniconda3/condabin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin"
trap "exit" TERM
