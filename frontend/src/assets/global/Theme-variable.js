// import { createTheme } from "@material-ui/core/styles";
import { createTheme } from "@mui/material/styles";
import typography from "./Typography";
import shadows from "./Shadows";

// ##############################

// // // Global Variables
// ##############################

const SidebarWidth = 257;   
const TopbarHeight = 70;

const baseTheme = createTheme({
  direction: "ltr",
  palette: {
    priority: {
        high: "#FD71AF",
        highBackground: "#FD71AF4D",
        medium: "#FFC800",
        mediumBackground: "#FFC8004D",
        low: "#93A0FF",
        lowBackground: "#93A0FF4D",
    },
    gray: {
        main: "#888793",
        light: "#F9F8FF",
    },
    text: {
        primary: "#3C3B40",
        secondary: "#9896A3",
        disabled: "#B7B7B7",
        danger: "#fc4b6c",
    },
    border: {
        main: "#E6E4F0",
    },
    primary: {
      main: "#000B58",
      light: "#e6f4ff",
    },
    pausebutton: {
        main: "#D4D2DC",
        contrastText: "#76747A",
    },
    endbutton: {
        // 30$ alpha for the background color
        main: "#EA34344D",
        contrastText: "#EA3434",
    },
    secondary: {
      main: "#006A67",
    },
    background: {
      default: "#fff",
    },
    success: {
      main: "#39cb7f",
      contrastText: "#ffffff",
    },
    danger: {
        main: "#fc4b6c",
        contrastText: "#ffffff",
    },
    error: {
      main: "#fc4b6c",
    },
    warning: {
      main: "#fdd43f",
      contrastText: "#ffffff",
    }
  },
  shape: {
    borderRadius: 5,
  },

  components: {
    MuiDivider: {
        styleOverrides: {
            root: {
                borderColor: "#E6E4F0",
            },
        },
    },
    MuiCssBaseline: {
      styleOverrides: {
        "*": {
          boxSizing: "border-box",
        },
        html: {
          height: "100%",
          width: "100%",
        },
        body: {
          height: "100%",
          margin: 0,
          padding: 0,
        },
        "#root": {
          height: "100%",
        },
      },
    },
    MuiContainer: {
      styleOverrides: {
        root: {
          paddingLeft: "15px !important",
          paddingRight: "15px !important",
          maxWidth: "1600px",
        },
      },
    },

    MuiButton: {
      styleOverrides: {
        root: {
            fontWeight: 600,
            textTransform: "none",
            boxShadow: "none",
            "&:hover": {
                boxShadow: "none",
            },
        },
      },
    },

    MuiListItem: {
      styleOverrides: {
        root: {
          borderRadius: "9px",
        },
      },
    },

    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: "20px",
          padding: "14px",
          margin: "15px",
        },
      },
    },

    MuiListItemIcon: {
      styleOverrides: {
        root: {
          minWidth: "40px",
        },
      },
    },

    MuiGridItem: {
      styleOverrides: {
        root: {
          paddingTop: "30px",
          paddingLeft: "30px !important",
        },
      },
    },

    MuiInputLabel: {
        styleOverrides: {
            root: {
                fontWeight: 500,
            },
        },
    }
  },
  mixins: {
    toolbar: {
      color: "#949db2",
      "@media(min-width:1280px)": {
        minHeight: TopbarHeight,
        padding: "0 30px",
      },
      "@media(max-width:1280px)": {
        minHeight: "64px",
      },
    },
  },
  status: {
    danger: "#e53e3e",
  },
  typography,
  shadows,
});

export { TopbarHeight, SidebarWidth, baseTheme };
