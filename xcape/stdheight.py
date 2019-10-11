
def stdheight(p_2d, t_2d, td_2d, p_s, t_s, td_s, pres_lev_pos, aglh0):
    
     aglh_2d, aglh_s1d = _stdheight(p_2d, t_2d, td_2d,
                                   p_s1d, t_s1d, td_s1d,
                                   pres_lev_pos, aglh0 = 2.,
                                   **kwargs)
    # nlev has to be the first dimension
    # nlev here is the number of levels in 3d variables (without surface level)
    nlev, ngrid = p_2d.shape
    # if above ground level height is 1 value
    # (i.e. 2m or 10m) generate ngrid-long array with aglh0
    if aglh0.shape[0]==1:
        aglh_in = np.ones(ngrid)*aglh0
        
    # type_grid  type of vertical grid: 1 for model levels, 2 for pressure levels:
    if type_grid == 1:
        from xcape import stdheight_2D_model_lev
        H2D, H_s  = stdheight_2D_model_lev.loop_stdheight(p_2d, t_2d, td_2d,
                                                      p_s, t_s, td_s,
                                                      aglh_in,
                                                      nlev, ngrid)
    elif type_grid == 2:
        from xcape import stdheight_2D_pressure_lev
        H2D, H_s  = stdheight_2D_pressure_lev.loop_stdheight(p_2d, t_2d, td_2d,
                                                      p_s, t_s, td_s,
                                                      aglh_in,pres_lev_pos,
                                                      nlev, ngrid)
        

    return H2D, H_s
