import json

class COCOConverter:
    def __init__(self, annotations=None, successful_batch_data=None):
        if annotations:
            self.annotations = annotations
        if successful_batch_data:
            self.successful_batch_data = successful_batch_data

    def is_annot_coco_format(self):
        """
        Check if the given annotations follow COCO format.
        COCO format contains "images", "annotations", and "categories" keys.
        """
        return all(key in self.annotations for key in ['images', 'annotations', 'categories'])
    
    def is_pred_coco_format(self):
        """
        Check if the given predictions follow COCO format.
        COCO format for predictions typically contains "image_id", "category_id", and "score" keys.
        """
        if isinstance(self.successful_batch_data, list) and len(self.successful_batch_data) > 0:
            # Check if the first item contains the necessary keys
            required_keys = {'image_id', 'category_id', 'score', 'loss'}
            return all(key in self.successful_batch_data[0] for key in required_keys)
        return False

    def convert_annotations(self):
        """
        Convert COCO annotations to the custom format used in the codebase.
        Custom format: { 'image_id': { 'annotation': [ ... ] } }
        """
        custom_annotations = {}

        # Loop through images in COCO format and add them to the custom format
        for image in self.annotations['images']:
            image_id = image['id']
            custom_annotations[image_id] = {"annotation": []}

        # Map COCO annotations to the custom format
        for annotation in self.annotations['annotations']:
            image_id = annotation['image_id']

            # Add annotation to the corresponding image_id in the custom format
            custom_annotations[image_id]['annotation'].append({
                'id': annotation['id'],
                'label': annotation['category_id']
            })

        return custom_annotations

    def convert_annot_if_needed(self):
        """
        Convert to custom format if the annotations are in COCO format.
        """
        if self.is_annot_coco_format():
            print("Annotations are in COCO format. Converting to custom format.")
            return self.convert_annotations()
        else:
            print("Annotations are already in custom format. No conversion needed.")
            return self.annotations
        
    def convert_pred_if_needed(self):
        """
        Convert to custom format if the annotations are in COCO format.
        """
        if self.is_pred_coco_format():
            print("Annotations are in COCO format. Converting to custom format.")
            return self.convert_predictions()
        else:
            print("Annotations are already in custom format. No conversion needed.")
            return self.successful_batch_data

    def convert_predictions(self):
        """
        Convert predictions from COCO format to the custom format.
        Custom format: { 'image_id': { 'image_id': ..., 'prediction_class': ..., 'confidence': ..., 'logits': [...], 'loss': ... } }
        """
        custom_predictions = {}
        
        for pred in self.successful_batch_data:
            image_id = pred['image_id']
            category_id = pred['category_id']
            confidence = pred['score']
            loss = pred.get('loss', None)

            # Initialize logits with zeros for two categories
            logits = [0.0, 0.0]
            logits[category_id] = confidence  # Set confidence at the index of category_id
            logits[1 - category_id] = 1 - confidence  # Set the remaining confidence value

            custom_predictions[image_id] = {
                'image_id': image_id,
                'prediction_class': category_id,
                'confidence': confidence,
                'logits': logits,
                'loss': loss
            }

        return custom_predictions
