export image_name=image_provider
export image_tag=1.0

docker build ./ -t $image_name:$image_tag

docker run --rm \
  --name $image_name \
  -e APP_NAME="Magma Image Bank" \
  -e VERSION="beta" \
  -e APP_DESCRIPTION="An app to store and serve images" \
  -e PORT=8000 \
  -p 8000:8000 \
  $image_name:$image_tag
