library(readr)
library(dplyr)
library(ggplot2)
library(MatchIt)
library(cobalt)

resolve_input_path <- function() {
  candidates <- c(
    "interview_prep/data_science_assignment/spotify_matching_input.csv",
    "spotify_matching_input.csv"
  )
  for (candidate in candidates) {
    if (file.exists(candidate)) {
      return(candidate)
    }
  }
  stop("spotify_matching_input.csv not found")
}

input_path <- resolve_input_path()

matching_df <- read_csv(input_path, show_col_types = FALSE) %>%
  mutate(genre_1 = factor(genre_1))

content_pc_cols <- grep("^content_pc", names(matching_df), value = TRUE)

match_terms <- c(
  "log_n_tracks",
  "log_n_local_tracks",
  "log_n_artists",
  "log_n_albums",
  content_pc_cols
)
content_pc_cols

match_formula <- as.formula(
  paste("is_spotify_owned ~", paste(match_terms, collapse = " + "))
)

mod_match <- matchit(
  formula = match_formula,
  data = matching_df,
  method = "nearest",
  distance = "glm",
  link = "logit",
  ratio = 3,
  estimand = "ATT",
  exact = ~ genre_1,
  replace = FALSE
)

sum_match <- summary(mod_match, un = TRUE)

bal <- bal.tab(mod_match, un = TRUE, drop.distance = TRUE, m.threshold = 0.1)
balance_table <- bal$Balance %>%
  as.data.frame() %>%
  tibble::rownames_to_column("covariate") %>%
  filter(Type != "Distance", covariate != "distance") %>%
  arrange(desc(abs(Diff.Un)))


matched_df <- match.data(mod_match, data = matching_df)

outcome_summary <- bind_rows(
  matching_df %>%
    group_by(segment) %>%
    summarise(
      sample = "Full sample",
      n = n(),
      median_monthly_stream30s = median(monthly_stream30s),
      median_non_owner_monthly_stream30s = median(non_owner_monthly_stream30s),
      .groups = "drop"
    ),
  matched_df %>%
    group_by(segment) %>%
    summarise(
      sample = "Matched sample",
      n = n(),
      median_monthly_stream30s = median(monthly_stream30s),
      median_non_owner_monthly_stream30s = median(non_owner_monthly_stream30s),
      .groups = "drop"
    )
)

outcome_plot_df <- bind_rows(
  matching_df %>%
    transmute(
      segment,
      sample = "Full sample",
      metric = "log1p(monthly_stream30s)",
      value = log_monthly_stream30s
    ),
  matching_df %>%
    transmute(
      segment,
      sample = "Full sample",
      metric = "log1p(non_owner_monthly_stream30s)",
      value = log_non_owner_monthly_stream30s
    ),
  matched_df %>%
    transmute(
      segment,
      sample = "Matched sample",
      metric = "log1p(monthly_stream30s)",
      value = log_monthly_stream30s
    ),
  matched_df %>%
    transmute(
      segment,
      sample = "Matched sample",
      metric = "log1p(non_owner_monthly_stream30s)",
      value = log_non_owner_monthly_stream30s
    )
)

outcome_distribution_plot <- ggplot(
  outcome_plot_df,
  aes(x = segment, y = value, fill = segment)
) +
  geom_violin(trim = FALSE, alpha = 0.35, color = NA) +
  geom_boxplot(width = 0.15, outlier.alpha = 0.15) +
  facet_grid(metric ~ sample) +
  labs(
    title = "Outcome distributions before and after matching",
    x = NULL,
    y = "Logged outcome",
    fill = NULL
  ) +
  theme_minimal(base_size = 12) +
  theme(legend.position = "none")

cat("Match formula:\n")
print(match_formula)

cat("\nSummary(mod_match, un = TRUE):\n")
print(sum_match)

cat("\nMatched sample sizes:\n")
print(table(matched_df$segment))

cat("\nOutcome summary:\n")
print(outcome_summary, n = nrow(outcome_summary))

cat("\nLargest pre-match SMDs:\n")
print(
  tibble::as_tibble(
    balance_table %>%
      select(covariate, Diff.Un, Diff.Adj) %>%
      slice_head(n = 15)
    ),
  n = 15
)

if (interactive()) {
  plot(mod_match, type = "jitter", interactive = FALSE)
  plot(
    mod_match,
    type = "density",
    interactive = FALSE,
    which.xs = ~ log_n_tracks + log_n_local_tracks + log_n_artists + log_n_albums
  )
  plot(mod_match, type = "hist")
  print(outcome_distribution_plot)
}
