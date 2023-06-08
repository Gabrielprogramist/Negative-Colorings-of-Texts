from django.shortcuts import render
from django.http import JsonResponse
from .forms import UserForm
from transformers import BertTokenizer, BertForSequenceClassification
import torch
import numpy as np

def index(request):
    if request.method == "POST":
        comment = request.POST.get("comment")
        model_name = 'Skoltech/russian-sensitive-topics'
        tokenizer = BertTokenizer.from_pretrained(model_name)
        model = BertForSequenceClassification.from_pretrained(model_name)
        import json
        with open(r"C:\django\metani\hello\static\js\id2topic.json") as f:
            target_vaiables_id2topic_dict = json.load(f)
        tokenized = tokenizer.batch_encode_plus([comment], max_length=512,
                                                pad_to_max_length=True,
                                                truncation=True,
                                                return_token_type_ids=False)
        tokens_ids, mask = torch.tensor(tokenized['input_ids']), torch.tensor(tokenized['attention_mask'])
        with torch.no_grad():
            model_output = model(tokens_ids, mask)

        def adjust_multilabel(y, is_pred=False):
            y_adjusted = []
            softmax = torch.nn.Softmax(dim=1)
            probabilities = softmax(y)
            top5_prob, top5_catid = torch.topk(probabilities, 5)
            for i in range(5):
                index = str(int(top5_catid[0][i]))
                y_c = target_vaiables_id2topic_dict[index]
                y_adjusted.append((y_c, top5_prob[0][i].item()))
            return y_adjusted

        preds = adjust_multilabel(model_output['logits'], is_pred=True)
        return JsonResponse({"classification": preds})
    else:
        userform = UserForm()
        return render(request, "index.html", {"form": userform})
def about(request):
    return render(request, "about.html")

def article(request):
    return render(request, "article.html")