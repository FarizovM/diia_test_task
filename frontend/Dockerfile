FROM node:20-alpine

WORKDIR /app

# Копіюємо package.json (створимо його пізніше при ініціалізації Vue)
# COPY package*.json ./
# RUN npm install

# Аналогічно, код буде монтуватися через volume
# COPY . .

CMD ["npm", "run", "dev", "--", "--host"]