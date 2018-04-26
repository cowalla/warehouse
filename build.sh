export WAREHOUSE_HOME="$(pwd)"
git clone git@github.com:cowalla/mediator.git
mv mediator crypto_mediator

docker build -t warehouse .

rm -rf crypto_mediator

# create external network
echo "Creating external network 'warehouse_network'"
docker network create warehouse_network