library(shiny)
library(sortable)

# Define IsColor function
IsSwitch <- function(input_string) {
  one <- grepl("1", input_string)
  two <- grepl("2", input_string)
  three <- grepl("3", input_string)
  four <- grepl("4", input_string)
  return(one & two & three & four)
}

# Define get_outcome function
get_outcome <- function(input_sequence, output_sequence) {
  map <- setNames(1:nchar(input_sequence), strsplit(input_sequence, NULL)[[1]])
  outcome <- sapply(strsplit(output_sequence, NULL)[[1]], function(o) map[[o]])
  return(paste0(outcome, collapse = ""))
}

compute <- function(formula) {
  # Split formula into fml and outcome
  parts <- strsplit(formula, "=")[[1]]
  fml <- strsplit(parts[1], "\\+")[[1]]
  outcome <- parts[2]
  
  # Predefined answer permutations
  answers <- c('1234', '1243', '1324', '1342', '1423', '1432', 
               '2134', '2143', '2314', '2341', '2413', '2431', 
               '3124', '3142', '3214', '3241', '3412', '3421', 
               '4123', '4132', '4213', '4231', '4312', '4321')

  # Define switch function
  switch_func <- function(a, b) {
    map <- setNames(seq_along(strsplit(a, NULL)[[1]]), strsplit(a, NULL)[[1]])
    new <- sapply(strsplit(b, NULL)[[1]], function(n) map[[as.character(n)]])
    return(paste0(new, collapse = ""))
  }
  
  # Loop through each answer and find the correct match
  for (a in answers) {
    fml_temp <- sapply(fml, function(x) gsub("x", a, x))
    out <- "1234"
    for (i in seq_along(fml_temp)) {
      out <- switch_func(out, fml_temp[i])
    }
    if (out == outcome) {
      break
    }
  }
  
  return(a)
}

shapes <- function(input_id){
  shapes = tags$div(
    tags$img(src="img/blue.png", style="width:50px; height:50px; margin: 5px;", `data-rank-id`="b"),
    tags$img(src="img/green.png", style="width:50px; height:50px; margin: 5px;", `data-rank-id`="g"),
    tags$img(src="img/red.png", style="width:50px; height:50px; margin: 5px;", `data-rank-id`="r"),
    tags$img(src="img/yellow.png", style="width:50px; height:50px; margin: 5px;", `data-rank-id`="y"),
    id=input_id
  )
  return(tagList(
    shapes,
    sortable_js(css_id = input_id,
    options = sortable_options(
      onSort = sortable_js_capture_input(input_id = input_id)
    ))
  ))
}

trim <- function(string) paste0(string, collapse = "")

IsComplete <- function(fml){
  if (fml == "") return("empty")
  if (fml == "x") return("shape")
  if (grepl("=", fml) ) {
    if(length(strsplit(fml, "=")[[1]])!=2) return("incomplete")
    outcome = trimws(strsplit(fml, "=")[[1]][2])
    first_part = strsplit(fml, "\\+")[[1]][1]
    if (nchar(outcome) == 4){
      if (IsSwitch(outcome) && (IsSwitch(first_part) | first_part == "x") ) {
        return("short")
      }  else if (sum(strsplit(first_part, "")[[1]] %in% strsplit(outcome, "")[[1]])==4) {
        return("long")
      } else {
        return("incomplete")
      }
    } else {
      return("incomplete")
    }
  } 
  if (!grepl("+", fml)) {
    return("incomplete")
  } else{
    parts <- strsplit(fml, "\\+")[[1]]
    if (!"x" %in% parts) return("incomplete")
    parts <- parts[parts != "x"]
    if (all(IsSwitch(parts))) {
      return ("shape")
    } else {
      return("incomplete")
    }
  }
}

ui <- fluidPage(
  tags$script(src = "app.js"),
  checkboxInput("shape_hide", "Hide Shapes"),
  conditionalPanel(condition = "!input.shape_hide", shapes("initial")),
  textInput("fml", "Formula (press `/~ to clear):"),
  verbatimTextOutput("text"),
  conditionalPanel(condition = "!input.shape_hide", shapes("final"))
)

server <- function(input, output, session) {

  observeEvent(input$keyid,{
    if(input$keyid == 96) { # clear input when ` or ~ is pressed
      updateTextInput(session, "fml", value = "")
    }
  })

  output$text <- renderText({
    type = IsComplete(input$fml)
    if (type == "incomplete") {
      ""
    } else if (type == "empty"){
      if(trim(input$initial)=="" | trim(input$final)=="") {
        ""
      } else {
        get_outcome(trim(input$initial), trim(input$final))
      }
    } else if (type == "short") {
      compute(input$fml)
    } else if (type == "long") {
      outcome = trimws(strsplit(input$fml, "=")[[1]][2])
      parts = strsplit(trimws(strsplit(input$fml, "=")[[1]][1]), "\\+")[[1]]
      outcome <- get_outcome(parts[1], outcome)
      parts <- parts[2:length(parts)]
      formula = paste0(parts, collapse = "+")
      formula = paste(formula, outcome, sep="=")
      compute(formula)
    } else if (type == "shape") {
      if(trim(input$initial)=="" | trim(input$final)=="") {
        "Please move the shapes"
      } else {
        #trim(input$initial)
        outcome <- get_outcome(trim(input$initial), trim(input$final))
        formula = paste(input$fml, outcome, sep="=")
        compute(formula)
      }
    }
  })

}

  shinyApp(ui, server)