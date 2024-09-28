# Solar-as-Judge

![Solar-as-Judge Demo](https://github.com/hunkim/solar-as-judge/assets/901975/738be829-1d20-4b9a-baad-e3f2c8d066c5)

Solar-as-Judge is a powerful Python package for evaluating and comparing AI-generated responses. It leverages the Upstage API to provide accurate and consistent judgments on the quality of AI outputs.

## Features

- Evaluate individual AI responses on a scale of 1-5
- Compare two AI responses and determine a winner
- Utilize ground truth for more accurate evaluations
- Ensure consistency through multiple trials

## Installation

```bash
pip install solar-as-judge
```

## Quick Start

### Single Answer Scoring

````python
import solar_as_judge as saj

prompt = "Please extract one keyword from this text: I love you so much"
ground_truth = "love"
answer = "love"

score = saj.get_judge_score(prompt, answer, ground_truth)
print(f"Score: {score}")
````


### A/B Testing

````python
import solar_as_judge as saj

prompt = "Please extract one keyword from this text: I love you so much"
ground_truth = "love"

A_answer = "love"
B_answer = "so much"

a_score, b_score = saj.judge(prompt, A_answer, B_answer, ground_truth)
print(f"Scores: A={a_score}, B={b_score}")
````


## API Reference

### `saj.get_judge_score(prompt, answer, ground_truth_answer, judge_llm=None, trials=3)`

Evaluates a single AI response.

- Returns: Integer score (1-5)

### `saj.judge(prompt, A_answer, B_answer, ground_truth=None, judge_llm=None, trials=7)`

Evaluates and compares two AI responses.

- Returns: Tuple of scores (A_score, B_score)

### `saj.get_winner(prompt, A_answer, B_answer, ground_truth_answer, judge_llm=None, trials=3)`

Determines the winner between two AI responses.

- Returns: String ("A" or "B")

## Configuration

Set the `UPSTAGE_API_KEY` environment variable with your key from the [Upstage console](https://console.upstage.ai).

## Examples

Check out the `test.py` file in the repository for more usage examples and test cases.

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, feature requests, or questions, please [open an issue](https://github.com/hunkim/solar-as-judge/issues) on our GitHub repository.
