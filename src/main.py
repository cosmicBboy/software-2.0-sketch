from functions import detect_spam


if __name__ == "__main__":
    data = [
        "What you doing?how are you?",
        "FreeMsg: Txt: CALL to No: 86888 & claim your reward of 3 hours talk time to use from your phone now! ubscribe6GBP/ mnth inc 3hrs 16 stop?txtStop",
    ]
    for x in data:
        output = detect_spam(x)
        proba = detect_spam(x, as_proba=True)
        print("\ndata:", x)
        print(f"output: {output}, probability: {proba}")
