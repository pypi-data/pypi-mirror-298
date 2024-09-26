import math
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
import numpy as np

from lazyplot.config import FigureConfig, DrawConfig

GLOBAL_CONFIG = FigureConfig()


#=======================================================================
def set_global_config(user_config):
    """
    set PlotConfig globally (not saved)
    """
    GLOBAL_CONFIG.override(user_config)
    return

#====================================================================
def generate_local_config(user_config):
    """
    regenerate PlotConfig for lazy_plot() and custom_plot()
    input: dict{ key of PlotConfig : value}
    output: PlotConfig override by user defined value 
    """
    cfg = GLOBAL_CONFIG
    cfg.override(user_config)
    return cfg

#================================================================================
def init_figure(num_axes: int, cfg):
    """
    make matplotlib.Figure and number of columns and rows for subplot
    """
    
    fig = plt.figure(figsize=cfg.figsize, linewidth=cfg.linewidth, layout=cfg.layout, dpi=cfg.dpi)
    ax_cols = cfg.columns
    ax_rows = math.ceil(num_axes /cfg.columns)
    
    return fig, ax_cols, ax_rows

#=================================================================================
def custom_plot(draw_config: list[DrawConfig],
                out_path: str = None,
                figure_config: dict | None = None):
    """
    Draw more detailed graph by using user-specified DrawConfig
    
    -------input-------
    draw_config (DrawConfig or list[DrawConfig]) > User-specified DrawConfig
    out_path (str or None) >  Output path of the image file. if None, no image file is output
    figure_config (dict) > Value to override FigureConfig.
    
    -------output------
    None
    
    """
    if isinstance(draw_config, list) == False:
        draw_config = [draw_config]
        
    cfg = generate_local_config(figure_config)
    fig, ax_cols, ax_rows = init_figure(len(draw_config), cfg)
    
    for i, data in enumerate(draw_config, 1):
        _ax = fig.add_subplot(ax_rows, ax_cols, i)
        plot_ax(_ax, data)
        
    if out_path is not None:
        fig.savefig(out_path, dpi=cfg.dpi)
    
    return

#=================================================================================
def lazy_plot(input_data: np.ndarray | list[np.ndarray], 
              out_path: str | None = None,
              figure_config: dict | None = None) :
    """
    Draw graphs by entering only data.
    
    -----input--------
    input_data (np.ndarray or list[np.ndarray]) > 
    out_path (str or None) >  Output path of the image file. if None, no image file is output
    figure_config (dict) > Value to override FigureConfig.
    
    -------output------
    None
    
    """
    if isinstance(input_data, list) is False:
        input_data = [input_data]
    
    cfg = generate_local_config(figure_config)    # local config within this function
    fig, ax_cols, ax_rows = init_figure(len(input_data), cfg)
    
    for i, data in enumerate(input_data, 1):
        _title = f'data {i}'
        _ax = fig.add_subplot(ax_rows, ax_cols, i)
        _draw_config = create_draw_config(data, _title, cfg)
        
        plot_ax(_ax, _draw_config)
        
    if out_path is not None:
        fig.savefig(out_path, dpi=cfg.dpi)
        
    return
        
#====================================================================================
def create_draw_config(data: np.ndarray, title: str, cfg: FigureConfig):
    
    if data.ndim == 1:
        plot_type = cfg.plot_type_1d
    elif data.ndim == 2:
        plot_type = cfg.plot_type_2d
    elif data.ndim == 3:
        plot_type = cfg.plot_type_3d
    else:
        raise ValueError("Invalid data dimension. Data is limited to 3 dimensions or less")
    
    draw_config = DrawConfig(y=data, plot_type=plot_type, title=title, linewidth=cfg.linewidth)
    
    return draw_config


#=======================================================================================
def plot_ax(ax: Axes, info: DrawConfig):
    
    require_legend = False
    
    match info.plot_type:
        #-------------------------------------------------------------------------------
        case "plot":
            if info.y.ndim > 2:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"plot\" require (N) or (M, N) data")
            
            if info.y.ndim == 1:
                info.y = np.expand_dims(info.y, axis=0)
                
            #plot----------------------------------------
            require_legend = True if len(info.y) != 1 else False
            for i, y in enumerate(info.y):
                _color = info.color[i % len(info.color)]
                _linestyle = info.line_style[(i // len(info.color)) % len(info.line_style)]
                _t = np.arange(len(y)) if info.t is None else info.t
                _label = f"graph {i+1}" if info.labels is None else info.labels[i]
                ax.plot(_t, y, label=_label, color=_color, alpha=info.alpha,
                        linewidth=info.linewidth, linestyle=_linestyle)
        #---------------------------------------------------------------------------------
        case "hist":
            if info.y.ndim != 1:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"hist\" require (N) data")
            ax.hist(info.y, color=info.color[0])
        #---------------------------------------------------------------------------------
        case "bar":
            if info.y.ndim != 1:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"bar\" require (N) data")
            label = [f"data {i + 1}" for i in range(len(info.y))] if info.labels is None else info.labels
            color = [info.color[i % len(info.color)] for i in range(len(info.y))]
            ax.bar(label, info.y, color=color)
            
        #----------------------------------------------------------------------------------
        case "boxplot":
            if info.y.ndim != 2:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"boxplot\" require (M, N) data")
            
            #plot--------------------
            label = [f"data {i + 1}" for i in range(len(info.y))] if info.labels is None else info.labels
            color = [info.color[i & len(info.color)] for i in range(len(info.y))]
            bplot = ax.boxplot(info.y.T, labels=label, patch_artist=True, medianprops=dict(color="white", linewidth=3))
            #paint facecolor
            for i, patch in enumerate(bplot['boxes']):
                color = info.color[i % len(info.color)]
                patch.set_facecolor(color)
            
        #----------------------------------------------------------------------------------
        case "scatter":
            if info.y.ndim == 1 or info.y.ndim > 3:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"scatter\" require (M, 2, N) or (2, N) data")
            elif info.y.ndim == 2:
                info.y = np.expand_dims(info.y, axis=0)
            
            if info.y.shape[1] != 2:
                print("WARNING: cannot plot 3D data. z or higher dimension axis is ignored. Valid shape of data is (M, 2, N) or (2, N)")
            
            #plot-----------------------------------------
            require_legend = True if len(info.y) != 1 else False
            for i, y in enumerate(info.y):
                _color = info.color[i % len(info.color)]
                _markerstyle = info.marker_style[(i // len(info.color)) % len(info.marker_style)]
                _label = f"graph {i+1}" if info.labels is None else info.labels[i]
                ax.scatter(y[0], y[1], label=_label, color=_color, alpha=info.alpha,
                        linewidth=info.linewidth, marker=_markerstyle)
        #--------------------------------------------------------------------------------    
        case "imshow":
            if info.y.ndim == 1 or info.y.ndim > 3:
                raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"imshow\" require (M, N) or (M, N, 3[RGB] | 4[RGBA]) data")
            
            if info.y.ndim == 3:
                if info.y.shape[2] != 3 and info.y.shape[2] != 4:
                    raise ValueError(f"Invalid data shape: {info.y.shape}. plot_type: \"imshow\" require (M, N) or (M, N, 3[RGB] | 4[RGBA]) data")
            
            #plot------------------------      
            ax.imshow(info.y)           
        #--------------------------------------------------------------------------------
        case _:
            raise ValueError(f"Invalid plot_type: {info.plot_type}.")
    
    
    # ax setting --------------------------------------
    if info.title is not None:
        ax.set_title(info.title)
    ax.set_xlabel(info.x_label)
    ax.set_ylabel(info.y_label)
    ax.set_xlim(info.x_lim)
    ax.set_ylim(info.y_lim)
    ax.set_aspect(info.aspect)
    
    if info.invert_xaxis:
        ax.invert_xaxis()
    if info.invert_yaxis:
        ax.invert_yaxis()
    if require_legend:   
        ax.legend()
    
#=======================================================================

if __name__ == "__main__":
    
    data = np.random.rand(30)