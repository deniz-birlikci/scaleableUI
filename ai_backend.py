import models

def evaluate_url(image_url):
    eval_model = models.EvalGPT()
    return eval_model.forward(image_url)

def compare_urls(source, target):
    compare_model = models.CompareGPT()
    return compare_model.forward(source, target)

def main(list_of_urls):
    # First, generate the evaluation on all the urls
    evaluation = []
    for image_url in list_of_urls:
        critique = evaluate_url(image_url)
        evaluation.append(critique)
        
    # Second, taking in the 0th element in the array as the source
    # image, do pairwise comparison between the 0th element and the rest
    comparisons = []
    source_image_url = list_of_urls[0]
    for target_image_url in list_of_urls[1:]:
        critique = compare_urls(source_image_url, target_image_url)
        comparisons.append(critique)
        
    return evaluation, comparisons